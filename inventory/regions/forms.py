# -*- coding: utf-8 -*-
#
# inventory/regions/forms.py
#
"""
Country, Language, and Timezone region forms.
"""
__docformat__ = "restructuredtext en"

from django import forms

from .models import Country, Language, TimeZone, Currency


#
# Country
#
class CountryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Set some fields to custom values.
        """
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget = forms.TextInput(
            attrs={'size': 2, 'maxlength': 2})

    class Meta:
        model = Country
        exclude = []


#
# Language
#
class LanguageForm(forms.ModelForm):
    """
    Language form
    """
    def __init__(self, request=None, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget = forms.TextInput(
            attrs={'size': 2, 'maxlength': 2})

    class Meta:
        model = Language
        exclude = []


#
# TimeZone
#
class TimeZoneForm(forms.ModelForm):
    """
    TimeZone form
    """
    def __init__(self, request=None, *args, **kwargs):
        super(TimeZoneForm, self).__init__(*args, **kwargs)
        self.fields['zone'].widget = forms.TextInput(
            attrs={'size': 2, 'maxlength': 2})
        self.fields['desc'].widget = forms.TextInput(
            attrs={'size': 50, 'maxlength': 100})

    class Meta:
        model = TimeZone
        exclude = []


#
# Currency
#
class CurrencyForm(forms.ModelForm):
    """
    Currency form
    """
    def __init__(self, request=None, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TimeZone
        exclude = []
