# -*- coding: utf-8 -*-
#
# inventory/locations/models.py
#
from __future__ import unicode_literals

"""
LocationSetName, LocationFormat, and LocationCode models.
"""
__docformat__ = "restructuredtext en"

import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from inventory.common import generate_public_key
from inventory.common.model_mixins import (
    UserModelMixin, TimeModelMixin, ValidateOnSaveMixin,)
from inventory.projects.models import Project

from .validation import FormatValidator

log = logging.getLogger('inventory.locations.models')


#
# LocationSetName
#
class LocationSetNameManager(models.Manager):

    def clone_set_name_tree(self, project, loc_set_name, user):
        """
        Gets and/or creates designated location set name with a new project,
        from the location set name provided, then creates all location formats
        as necessary. Returns a list of objects or an empty list if the new
        location set name already existed.
        """
        node_list = []

        if loc_set_name.shared and project.has_authority(user):
            kwargs = {}
            kwargs['description'] = loc_set_name.description
            kwargs['shared'] = loc_set_name.shared
            kwargs['separator'] = loc_set_name.separator
            kwargs['creator'] = user
            kwargs['updater'] = user
            obj, created = self.get_or_create(
                project=project, name=loc_set_name.name, defaults=kwargs)

            if created:
                node_list.append(obj)

                for fmt_obj in loc_set_name.location_formats.all():
                    kwargs = {}
                    kwargs['segment_order'] = fmt_obj.segment_order
                    kwargs['description'] = fmt_obj.description
                    kwargs['creator'] = user
                    kwargs['updater'] = user
                    node, created = LocationFormat.objects.get_or_create(
                        location_set_name=obj,
                        char_definition=fmt_obj.char_definition,
                        defaults=kwargs)
                    node_list.append(node)
            else:
                msg = _("The '{}' record already exists, cannot clone."
                        ).format(obj)
                log.error(msg)
                raise ValueError(msg)
        else:
            msg = _("To clone the '{}' location objects they must be shared "
                    "and the user must have authority."
                    ).format(loc_set_name.name)
            log.error(msg)
            raise ValueError(msg)

        return node_list

    def delete_set_name_tree(self, project, loc_set_name, user):
        """
        Deletes the set name tree starting with any location code objects,
        continuing with location format objects, then deleting the location
        set name object itself. Since this is a full removal of an entire tree
        it will invalidate any items that used any location code objects.
        """
        deleted_nodes = []

        for fmt in loc_set_name.location_formats.all():
            child_nodes = []

            for code in fmt.location_codes.all():
                child_nodes += self._recurse_children(code)

            fmt_obj = [fmt.char_definition, child_nodes]
            fmt.delete()
            deleted_nodes.append(fmt_obj)

        deleted_nodes.insert(0, loc_set_name.name)
        loc_set_name.delete()
        return deleted_nodes

    def _recurse_children(self, child):
        deleted_nodes = []

        for c in child.children.all():
            if c.children.count():
                deleted_nodes += self._recurse_children(c)
            else:
                deleted_nodes.append(c.path)
                c.delete()

        return deleted_nodes


@python_2_unicode_compatible
class LocationSetName(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
        )

    public_id = models.CharField(
        verbose_name=_("Public Location Set Name ID"), max_length=30,
        unique=True, blank=True,
        help_text=_("Public ID to identify an individual project."))
    name = models.CharField(
        verbose_name=_("Name"), max_length=100,
        help_text=_("Enter a name for this series of formats."))
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name=_("Project"),
        related_name='location_set_names', db_index=False,
        help_text=_("The project that owns this record."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=1000, null=True, blank=True,
        help_text=_("Define what the codes derived from this format are used "
                    "for."))
    shared = models.BooleanField(
        verbose_name=_("Shared"), choices=YES_NO, default=YES,
        help_text=_("If you would like others to make a copy of your formats."))
    separator = models.CharField(
        verbose_name=_("Segment Separator"), max_length=3, default=':',
        help_text=_("The separator to use between segments. Defaults to a "
                    "colon (:). Max length is three characters."))

    objects = LocationSetNameManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

        # Check the length of the separator.
        FormatValidator(self.separator)

    def save(self, *args, **kwargs):
        super(LocationSetName, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name',)
        ordering = ('project__name',)
        verbose_name = _("Location Set Name")
        verbose_name_plural = _("Location Set Names")


@receiver(post_save, sender=LocationSetName)
def set_root_objects(sender, **kwargs):
    """
    Create this set name's root format and code.
    """
    instance = kwargs.get('instance')

    if instance:
        kwargs = {}
        kwargs['description'] = ("This is the root format for the root code "
                                 "in this project.")
        kwargs['creator'] = instance.creator
        kwargs['updater'] = instance.updater
        lf, created = LocationFormat.objects.get_or_create(
            location_set_name=instance,
            char_definition=LocationCode.ROOT_NAME, defaults=kwargs)

        if created:
            kwargs.pop('description', None)
            LocationCode.objects.create(
                location_format=lf, segment=LocationCode.ROOT_NAME, **kwargs)


#
# LocationFormat
#
class LocationFormatManager(models.Manager):

    def get_root_format(self, loc_set_name):
        """
        Returnds the auto generated root LocationFormat object.
        """
        try:
            return self.get(location_set_name=loc_set_name,
                            char_definition=LocationCode.ROOT_NAME)
        except LocationFormat.DoesNotExist as e:
            msg = _("Root format does not exist for set name '{}'."
                    ).format(loc_set_name)
            log.error(msg)
            raise LocationFormat.DoesNotExist(msg)

    def get_char_definition(self, project, name, fmt):
        record = None

        try:
            record = self.get(location_set_name__name=name,
                              location_set_name__project=project,
                              char_definition=fmt)
        except self.model.DoesNotExist:
            # The record does not exist, so return None.
            pass

        return record


@python_2_unicode_compatible
class LocationFormat(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):

    public_id = models.CharField(
        verbose_name=_("Public Location Format ID"), max_length=30,
        unique=True, blank=True,
        help_text=_("Public ID to identify an individual project."))
    location_set_name = models.ForeignKey(
        LocationSetName, on_delete=models.CASCADE, db_index=False,
        verbose_name=_("Location Set Name"), related_name="location_formats",
        help_text=_("The location set name relative to this location format."))
    segment_length = models.PositiveIntegerField(
        verbose_name=_("Segment Length"), editable=False, default=0,
        help_text=_("The length of this character definition."))
    char_definition = models.CharField(
        verbose_name=_("Format"), max_length=250, db_index=True,
        help_text=_("Determine the character position definition where "
                    "alpha='\\a', numeric='\\d', punctuation='\\p', or "
                    "any hard coded character. ex. \\a\\d\\d\\d could be "
                    "B001 or \\a@\d\d could be D@99."))
    segment_order =  models.PositiveIntegerField(
        verbose_name=_("Segment Order"), default=0,
        help_text=_("A number indicating the order that this segment will "
                    "appear in the location code. Numbers should start "
                    "with 0 (Can be edited in the list view also)."))
    description = models.CharField(
        verbose_name=_("Description"), max_length=1000, null=True, blank=True,
        help_text=_("Enter a description of the category segments."))

    objects = LocationFormatManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

        # Set the char_definition after checking it's validity.
        self.char_definition = FormatValidator(
            self.location_set_name.separator
            ).validate_char_definition(self.char_definition)

        # Set the segment_length.
        self.segment_length = len(self.char_definition.replace('\\', ''))

    def save(self, *args, **kwargs):
        super(LocationFormat, self).save(*args, **kwargs)

    def __str__(self):
        return self.char_definition

    class Meta:
        unique_together = ('location_set_name', 'char_definition',)
        ordering = ('segment_order',)
        verbose_name = _("Location Format")
        verbose_name_plural = _("Location Formats")


#
# LocationCode
#
class LocationCodeManager(models.Manager):

    def get_root_code(self, loc_set_name):
        """
        Returnds the auto generated root LocationFormat object.
        """
        loc_fmt = LocationFormat.objects.get_root_format(loc_set_name)

        try:
            return loc_fmt.location_codes.get(segment=LocationCode.ROOT_NAME)
        except LocationCode.DoesNotExist as e:
            msg = _("Root code does not exist for set name '{}'."
                    ).format(loc_set_name)
            log.error(msg)
            raise LocationCode.DoesNotExist(msg)

    def get_parents(self, fmt_obj):
        parents = self._recurse_parents(fmt_obj)
        parents.reverse()
        return parents

    def _recurse_parents(self, fmt_obj):
        parents = []

        if fmt_obj.parent_id:
            parents.append(fmt_obj.parent)
            more = self._recurse_parents(fmt_obj.parent)
            parents.extend(more)

        return parents

    def get_all_root_trees(self, project, segment):
        result = []
        records = self.select_related('parent').filter(
            segment=segment,
            location_format__location_set_name__project=project)

        if len(records) > 0:
            result[:] = [self.get_parents(record) for record in records]

        return result


@python_2_unicode_compatible
class LocationCode(TimeModelMixin, UserModelMixin, ValidateOnSaveMixin):
    ROOT_NAME = '#'

    public_id = models.CharField(
        verbose_name=_("Public Location Code ID"), max_length=30,
        unique=True, blank=True,
        help_text=_("Public ID to identify an individual project."))
    location_format = models.ForeignKey(
        LocationFormat, on_delete=models.CASCADE, verbose_name=_("Format"),
        related_name="location_codes", db_index=False,
        help_text=_("Choose the format that this segment will be based on."))
    segment = models.CharField(
        verbose_name=_("Segment"), max_length=250,
        help_text=_("See the LocationFormat.description for the "
                    "format used."))
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, verbose_name=_("Parent"),
        db_index=False, blank=True, null=True, default=None,
        related_name='children', help_text=_("The parent of this segment."))
    path = models.CharField(
        verbose_name=_("Path"), max_length=1000, editable=False,
        help_text=_("The full hierarchical path of this segment."))
    level = models.SmallIntegerField(
        verbose_name=_("Level"), editable=False,
        help_text=_("The location in the hierarchy of this segment."))

    objects = LocationCodeManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

        # Test max length, is not None, and format validity of segment.
        separator = self.location_format.location_set_name.separator

        self.segment = FormatValidator(
            separator, fmt=self.location_format.char_definition
            ).validate_segment(self.segment)

        # Test that a segment is not a parent to itself.
        parents = LocationCode.objects.get_parents(self)

        if self.segment in [parent.segment for parent in parents]:
            raise ValidationError({
                'parent': _("You cannot have a segment as a child to itself.")
                })

        # Test that all segments have the same location set name.
        set_name = self.location_format.location_set_name.name

        if not all([set_name == parent.location_format.location_set_name.name
                    for parent in parents]):
            raise ValidationError({
                'location_set_name': _("All segments must be derived from the "
                                       "same location set name.")})

        # Test that the number of segments defined are equal to or less than
        # the number of formats for this location set name.
        max_num_segments = (self.location_format.location_set_name.
                            location_formats.count())
        length = len(parents) + 1 # Parents plus self.

        if length > max_num_segments:
            raise ValidationError({
                'segment': _("There are more segments than defined formats, "
                             "found: {}, allowed: {}").format(
                    length, max_num_segments)
                })

        # Set the path and level.
        self.path = self._get_category_path()
        self.level = self.path.count(separator)

    def save(self, *args, **kwargs):
        super(LocationCode, self).save(*args, **kwargs)

        # Fix all the children if any.
        iterator = self.children.iterator()

        try:
            while True:
                child = six.next(iterator)
                child.save()
        except StopIteration:
            pass

    def __str__(self):
        return self.segment

    class Meta:
        unique_together = ('location_format', 'parent', 'segment',)
        ordering = ('path',)
        verbose_name = _("Location Code")
        verbose_name_plural = _("Location Codes")

    def get_separator(self):
        return self.location_format.location_set_name.separator

    def _get_category_path(self, current=True):
        parents = LocationCode.objects.get_parents(self)
        if current: parents.append(self)
        return self.get_separator().join([parent.segment for parent in parents])

    def parents_producer(self):
        return self._get_category_path(current=False)
    parents_producer.short_description = _("Segment Parents")

    def char_def_producer(self):
        return self.location_format.char_definition
    char_def_producer.short_description = _("Character Definition")


@receiver(pre_save, sender=LocationCode)
def create_parent(sender, **kwargs):
    instance = kwargs.get('instance')

    if (instance and instance.parent is None and
        instance.segment != LocationCode.ROOT_NAME):
        # Find the ROOT format
        lf = instance.location_format.location_set_name.location_formats.get(
            char_definition=LocationCode.ROOT_NAME)
        # Set the parent to the ROOT code.
        instance.parent = LocationCode.objects.get(
            location_format=lf, parent=None, segment=LocationCode.ROOT_NAME)
