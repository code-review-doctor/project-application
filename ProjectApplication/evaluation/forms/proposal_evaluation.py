from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from project_core.widgets import XDSoftYearMonthDayPickerInput
from ..models import ProposalEvaluation


class ProposalEvaluationForm(forms.ModelForm):
    FORM_NAME = 'proposal_evaluation_form'

    def __init__(self, *args, **kwargs):
        assert 'instance' not in kwargs

        self._proposal = kwargs.pop('proposal')

        try:
            proposal_evaluation = ProposalEvaluation.objects.get(proposal=self._proposal)
            kwargs['instance'] = proposal_evaluation
        except ObjectDoesNotExist:
            pass

        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('logged-proposal-evaluation', kwargs={'uuid': self._proposal.uuid})
        self.helper.add_input(Submit('submit', 'Save evaluation', css_class='btn-primary'))

        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['decision_date'])
        self.fields['proposal'].initial = self._proposal

    def clean(self):
        # TODO: Check proposal is eligible - else this should not be displayed anyway
        pass

    def save(self, *args, **kwargs):
        user = kwargs.pop('user')

        # TODO: check user has permission to save
        return super().save(*args, **kwargs)

    class Meta:
        model = ProposalEvaluation

        fields = ['proposal', 'final_mark', 'allocated_budget', 'panel_remarks', 'feedback_to_applicant', 'panel_recommendation',
                  'board_decision', 'decision_date']
        widgets = {
            'proposal': forms.HiddenInput,
            'decision_date': XDSoftYearMonthDayPickerInput
        }
