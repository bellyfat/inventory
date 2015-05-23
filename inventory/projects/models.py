#
# inventory/projects/models.py
#

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from dcolumn.common.model_mixins import (
    UserModelMixin, TimeModelMixin, StatusModelMixin, StatusModelManagerMixin)


class ProjectManager(StatusModelManagerMixin):
    pass


class Project(TimeModelMixin, UserModelMixin, StatusModelMixin):
    """
    This model implements project functionality.
    """
    YES = True
    NO = False
    PUBLIC_BOOL = (
        (YES, _('Yes')),
        (NO, _('No')),
        )

    name = models.CharField(
        verbose_name=_("Project Name"), max_length=256)
    members = models.ManyToManyField(
        User, verbose_name=_("Project Members"), blank=True)
    public = models.BooleanField(
        verbose_name=_("Public"), choices=PUBLIC_BOOL, default=YES)

    objects = ProjectManager()

    class Meta:
        ordering = ('name',)
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __unicode__(self):
        return self.name