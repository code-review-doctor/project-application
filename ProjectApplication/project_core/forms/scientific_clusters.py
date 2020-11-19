from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.http import QueryDict

from project_core.forms.person import PersonForm
from project_core.models import Proposal, ProposalScientificCluster


class ScientificClusterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: pass data
        self._person_form = self._get_person_form()

        self.helper = FormHelper()
        self.helper.form_tag = False

        # self.helper.disable_csrf = True  # checked in the higher form level

        self.helper.layout = Layout(
            Div(
                Div('proposal', hidden=True),
                Div('id', hidden=True),
                Div(Field('DELETE', hidden=True)),
                css_class='row', hidden=True
            ),
            Div(
                Div('title', css_class='col-12'),
                css_class='row'
            ),

            *self._person_form.helper.layout
        )
        self.fields.update(self._person_form.fields)


    def _get_person_form(self):
        # This is a QueryDict, not a dict
        person_form_data = self.data.copy()
        person_form_data.clear()

        # to get the fields
        temporary_person_form = PersonForm()

        for field_name in self.data.keys():
            if field_name in ['encoding', 'csrfmiddlewaretoken']:
                person_form_data.setlist(field_name, self.data.getlist(field_name))

            if not field_name.startswith(self.prefix):
                continue

            person_form_field_name = field_name[len(f'{self.prefix}-'):]

            if person_form_field_name in temporary_person_form.fields:
                person_form_data.setlist(person_form_field_name, self.data.getlist(field_name))

        person = PersonForm(data=person_form_data)
        return person

    def is_valid(self):
        scientific_cluster_is_valid = super().is_valid()

        return scientific_cluster_is_valid and self._person_form.is_valid()

    def clean(self):
        cd = super().clean()
        return cd

    def save(self, *args, **kwargs):
        sub_pi = self._person_form.save_person()

        instance = super().save(commit=False)
        instance.sub_pi = sub_pi

        return instance.save()

    class Meta:
        model = ProposalScientificCluster
        fields = ['proposal', 'title']


class ScientificClustersFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_queryset(self):
        return super().get_queryset().order_by('id')

    def save(self, *args, **kwargs):
        self.is_valid()
        return super().save(*args, **kwargs)


ScientificClustersInlineFormSet = inlineformset_factory(Proposal, ProposalScientificCluster, form=ScientificClusterForm,
                                                        formset=ScientificClustersFormSet,
                                                        min_num=1, extra=0, can_delete=True)
