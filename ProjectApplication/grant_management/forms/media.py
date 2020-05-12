from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from dal import autocomplete
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from grant_management.models import Medium
from project_core.models import Project
from project_core.widgets import XDSoftYearMonthDayPickerInput


class MediumModelForm(forms.ModelForm):
    FORM_NAME = 'medium'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['received_date'])

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True  # checked in the higher form level

        self.helper.layout = Layout(
            Div(
                Div('project', hidden=True),
                Div('id', hidden=True),
                Div(Field('DELETE', hidden=True)),
                css_class='row', hidden=True
            ),
            Div(
                Div('photographer', css_class='col-4'),
                Div('license', css_class='col-4'),
                Div('copyright', css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div('blog_posts', css_class='col-6'),
                Div('file', css_class='row-6'),
                css_class='row'
            )
        )

    def clean(self):
        cd = super().clean()

    class Meta:
        model = Medium
        fields = ['project', 'received_date', 'photographer', 'license', 'copyright', 'blog_posts', 'file',
                  'descriptive_text']
        widgets = {'due_date': XDSoftYearMonthDayPickerInput,
                   'photographer': autocomplete.ModelSelect2(url='logged-autocomplete-physical-people')}


class MediaFormSet(BaseInlineFormSet):
    FORM_NAME = 'media_form'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = MediaFormSet.FORM_NAME

    def get_queryset(self):
        return super().get_queryset().order_by('received_date')


MediaInlineFormSet = inlineformset_factory(Project, Medium, form=MediumModelForm,
                                           formset=MediaFormSet,
                                           min_num=1, extra=0, can_delete=True)
