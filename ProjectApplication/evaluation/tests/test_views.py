from datetime import datetime, date

from django.test import TestCase
from django.urls import reverse

from ProjectApplication import settings
from evaluation.models import ProposalEvaluation, CallEvaluation, Criterion
from evaluation.views import CallEvaluationValidation
from project_core.models import Proposal, ProposalStatus, Project
from project_core.tests import database_population
from project_core.tests.utils_for_tests import dict_to_multivalue_dict


class CallEvaluationSummaryViewTest(TestCase):
    def setUp(self):
        pass

    def test_check_all_submitted_proposals_have_eligibility(self):
        proposal = database_population.create_proposal()

        proposal.eligibility = Proposal.ELIGIBILITYNOTCHECKED
        proposal.proposal_status = ProposalStatus.objects.get(name=settings.PROPOSAL_STATUS_SUBMITTED)
        proposal.save()

        proposals = Proposal.objects.filter(uuid=proposal.uuid)

        # Expects one Proposal that is submitted but eligibility not checked...
        check_result = CallEvaluationValidation._check_all_submitted_proposals_have_eligibility_set(proposals)
        self.assertEqual(check_result['proposals'].count(), 1)
        self.assertEqual(check_result['proposals'][0], proposal)

        # Sets it not eligible
        proposal.eligibility = Proposal.NOTELIGIBLE
        proposal.save()

        # Then all good for this test
        check_result = CallEvaluationValidation._check_all_submitted_proposals_have_eligibility_set(proposals)
        self.assertEqual(check_result['proposals'].count(), 0)

    def test_check_eligible_proposals_have_evaluation(self):
        proposal = database_population.create_proposal()

        proposal.eligibility = Proposal.ELIGIBILITYNOTCHECKED
        proposal.proposal_status = ProposalStatus.objects.get(name=settings.PROPOSAL_STATUS_SUBMITTED)
        proposal.save()

        proposals = Proposal.objects.filter(uuid=proposal.uuid)

        # Expects one proposal that is eligible but doesn't have a proposal evaluation
        check_result = CallEvaluationValidation._check_all_submitted_proposals_have_eligibility_set(proposals)
        self.assertEqual(check_result['proposals'].count(), 1)

        proposal_evaluation = ProposalEvaluation()
        proposal_evaluation.proposal = proposal
        proposal_evaluation.save()

        proposal.eligibility = Proposal.ELIGIBLE
        proposal.save()

        proposals = Proposal.objects.filter(uuid=proposal.uuid)

        # Now it has the proposal evaluation, it's all good
        check_result = CallEvaluationValidation._check_all_submitted_proposals_have_eligibility_set(proposals)
        self.assertEqual(check_result['proposals'].count(), 0)


class ProposalEvaluationUpdateTest(TestCase):
    def setUp(self):
        self._proposal = database_population.create_proposal()

        self._call_evaluation = CallEvaluation()
        self._call_evaluation.call = self._proposal.call
        self._call_evaluation.panel_date = datetime.today()
        self._call_evaluation.save()

        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(
            reverse('logged-proposal-evaluation-add') + f'?proposal={self._proposal.id}')

        self.assertEqual(response.status_code, 200)

    def test_proposal_evaluation_detail_permission_denied(self):
        client = database_population.create_reviewer_logged_client()

        response = client.get(reverse('logged-proposal-evaluation-add') + f'?proposal={self._proposal.id}')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('accounts-login')))

    def test_proposal_evaluation_post_permission_denied(self):
        client = database_population.create_reviewer_logged_client()

        response = client.post(reverse('logged-proposal-evaluation-add'), kwargs={'pk': self._proposal.id})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('accounts-login')))

    def test_proposal_evaluation_create(self):
        reviewer = database_population.create_reviewer()

        data = dict_to_multivalue_dict({'proposal_evaluation_form-proposal': self._proposal.id,
                                        'proposal_evaluation_form-reviewers': [reviewer.id]})

        response = self._client_management.post(
            reverse('logged-proposal-evaluation-update', kwargs={'pk': self._proposal.id}),
            data=data)

        self.assertEqual(response.status_code, 200)

    def test_proposal_evaluation_update_post_permission_denied(self):
        client = database_population.create_management_logged_client()

        self._create_proposal_evaluation(self._proposal)
        self._call_evaluation.close(database_population.create_management_user())

        response = client.post(reverse('logged-proposal-evaluation-update', kwargs={'pk': self._proposal.id}))

        self.assertEqual(response.status_code, 403)

    def test_proposal_evaluation_update_get_permission_denied(self):
        client = database_population.create_management_logged_client()

        self._create_proposal_evaluation(self._proposal)

        self._call_evaluation.close(database_population.create_management_user())

        response = client.get(
            reverse('logged-proposal-evaluation-update', kwargs={'pk': self._proposal.proposalevaluation.id}))

        self.assertEqual(response.status_code, 403)

    @staticmethod
    def _create_proposal_evaluation(proposal):
        proposal_evaluation = ProposalEvaluation()
        proposal_evaluation.proposal = proposal
        proposal_evaluation.board_decision = ProposalEvaluation.BOARD_DECISION_FUND
        proposal_evaluation.panel_recommendation = ProposalEvaluation.PANEL_RECOMMENDATION_FUND
        proposal_evaluation.allocated_budget = 20_000
        proposal_evaluation.save()


class ProposalEvaluationListTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(reverse('logged-evaluation-list'))

        self.assertEqual(response.status_code, 200)


class CallEvaluationUpdateTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()
        self._reviewer = database_population.create_reviewer()
        self._criteria = database_population.create_evaluation_criteria()

    def test_get(self):
        call_evaluation = CallEvaluation()
        call_evaluation.call = self._proposal.call
        call_evaluation.panel_date = datetime.today()
        call_evaluation.save()

        response = self._client_management.get(
            reverse('logged-call-evaluation-update', kwargs={'pk': call_evaluation.id}))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = dict_to_multivalue_dict({'call_evaluation_form-call': self._proposal.call.id,
                                        'call_evaluation_form-panel_date': '16-03-2020',
                                        'call_evaluation_form-evaluation_sheet': [''],
                                        'call_evaluation_form-reviewers': [self._reviewer.id],
                                        'call_evaluation_form-criteria': [self._criteria[0].id],
                                        'save': 'Save Call Evaluation'})

        self.assertEqual(CallEvaluation.objects.all().count(), 0)

        response = self._client_management.post(
            reverse('logged-call-evaluation-add') + f'?call={self._proposal.call.id}', data=data)

        call_evaluation = self._proposal.call.callevaluation

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('logged-call-evaluation-detail', kwargs={'pk': call_evaluation.id}))
        self.assertEqual(CallEvaluation.objects.all().count(), 1)
        self.assertEqual(call_evaluation.panel_date, date(2020, 3, 16))

    def test_post_permission_denied(self):
        reviewer_client = database_population.create_reviewer_logged_client()

        data = dict_to_multivalue_dict({'call_evaluation_form-call': self._proposal.call.id,
                                        'call_evaluation_form-panel_date': '16-03-2020',
                                        'call_evaluation_form-evaluation_sheet': [''],
                                        'save': 'Save Call Evaluation'})

        response = reviewer_client.post(
            reverse('logged-call-evaluation-add') + f'?call={self._proposal.call.id}', data=data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('accounts-login')))


class ProposalListTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(
            reverse('logged-call-evaluation-list-proposals', kwargs={'call_id': self._proposal.call.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['call'], self._proposal.call)
        self.assertEqual(response.context['proposals'].count(), 0)


class ProposalEvaluationDetailTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        proposal_evaluation = ProposalEvaluation()
        proposal_evaluation.proposal = self._proposal
        proposal_evaluation.save()

        response = self._client_management.get(
            reverse('logged-proposal-evaluation-detail', kwargs={'pk': proposal_evaluation.id}))

        self.assertEqual(response.status_code, 200)


class CallEvaluationDetailTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_get_context_data(self):
        call_evaluation = CallEvaluation()
        call_evaluation.call = self._proposal.call
        call_evaluation.panel_date = datetime.today()
        call_evaluation.save()

        response = self._client_management.get(
            reverse('logged-call-evaluation-detail', kwargs={'pk': call_evaluation.id}))

        self.assertEqual(response.status_code, 200)


class ProposalDetailTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(
            reverse('logged-call-evaluation-proposal-detail', kwargs={'pk': self._proposal.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['force_eligibility_form_displayed'])


class CallEvaluationSummaryTest(TestCase):
    def setUp(self):
        self._user = database_population.create_management_user()
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(
            reverse('logged-call-evaluation-summary', kwargs={'call_id': self._proposal.call.id}))

        self.assertEqual(response.status_code, 200)


class CallEvaluationValidationTest(TestCase):
    def setUp(self):
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_get_context_data(self):
        proposal_submitted = ProposalStatus.objects.get(name=settings.PROPOSAL_STATUS_SUBMITTED)
        self._proposal.proposal_status = proposal_submitted
        self._proposal.save()

        call_evaluation = CallEvaluation()
        call_evaluation.call = self._proposal.call
        call_evaluation.panel_date = datetime.today()
        call_evaluation.save()

        # Checks that 1 proposal, 0 eligible...
        response = self._client_management.get(
            reverse('logged-call-evaluation-validation', kwargs={'call_id': self._proposal.call.id}))

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['all_good'], False)
        self.assertEqual(context['can_close'], False)
        self.assertEqual(context['total_number_of_submitted'], 1)
        self.assertEqual(context['total_number_of_eligible'], 0)
        self.assertEqual(context['total_number_of_funded'], 0)
        self.assertEqual(context['total_number_of_eligible_not_funded'], 0)

        # Makes the proposal eligible
        self._proposal.eligibility = Proposal.ELIGIBLE
        self._proposal.save()

        # Checks that 1 proposal, 1 eligible, 0 funded
        response = self._client_management.get(
            reverse('logged-call-evaluation-validation', kwargs={'call_id': self._proposal.call.id}))

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['all_good'], False)
        self.assertEqual(context['can_close'], False)
        self.assertEqual(context['total_number_of_submitted'], 1)
        self.assertEqual(context['total_number_of_eligible'], 1)
        self.assertEqual(context['total_number_of_funded'], 0)
        self.assertEqual(context['total_number_of_eligible_not_funded'], 1)

        # Funds the proposal. In reality the form would force the attached letter before it's funded, etc.
        # but here accessing to the model straight away all the rest is not needed
        proposal_evaluation = ProposalEvaluation()
        proposal_evaluation.proposal = self._proposal
        proposal_evaluation.board_decision = ProposalEvaluation.BOARD_DECISION_FUND
        proposal_evaluation.save()

        # Checks that 1 proposal, 1 eligible, 1 funded
        response = self._client_management.get(
            reverse('logged-call-evaluation-validation', kwargs={'call_id': self._proposal.call.id}))

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context['all_good'], False)
        self.assertEqual(context['can_close'], False)
        self.assertEqual(context['total_number_of_submitted'], 1)
        self.assertEqual(context['total_number_of_eligible'], 1)
        self.assertEqual(context['total_number_of_funded'], 1)
        self.assertEqual(context['total_number_of_eligible_not_funded'], 0)


class CallCloseEvaluationTest(TestCase):
    def setUp(self):
        self._client = database_population.create_management_logged_client()
        self._proposal = database_population.create_proposal()

    def test_post(self):
        call_evaluation = CallEvaluation()
        call_evaluation.call = self._proposal.call
        call_evaluation.panel_date = datetime.today()
        call_evaluation.save()

        # Makes the proposal eligible
        self._proposal.eligibility = Proposal.ELIGIBLE
        self._proposal.save()

        # Funds the proposal. In reality the form would force the attached letter before it's funded, etc.
        # but here accessing to the model straight away all the rest is not needed
        proposal_evaluation = ProposalEvaluation()
        proposal_evaluation.proposal = self._proposal
        proposal_evaluation.board_decision = ProposalEvaluation.BOARD_DECISION_FUND
        proposal_evaluation.allocated_budget = 20_000
        proposal_evaluation.save()

        self.assertEqual(Project.objects.all().count(), 0)

        response = self._client.post(
            reverse('logged-call-close-evaluation', kwargs={'call_id': self._proposal.call.id}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Project.objects.all().count(), 1)

        # Verifies created project
        project = Project.objects.all()[0]

        self.assertEqual(project.title, self._proposal.title)
        self.assertEqual(project.location, self._proposal.location)
        self.assertEqual(project.start_date, self._proposal.start_date)
        self.assertEqual(project.end_date, self._proposal.end_date)
        self.assertEqual(project.principal_investigator, self._proposal.applicant)
        self.assertEqual(project.principal_investigator, self._proposal.applicant)

        self.assertEqual(project.overarching_project, self._proposal.overarching_project)
        self.assertEqual(project.allocated_budget, self._proposal.proposalevaluation.allocated_budget)
        self.assertEqual(project.status, Project.ONGOING)

        self.assertEqual(project.call, self._proposal.call)
        self.assertEqual(project.proposal, self._proposal)

        # TODO: check project.geographical_areas and project.keywords


class ProposalEligibilityUpdateTest(TestCase):
    def setUp(self):
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_post(self):
        self.assertEqual(self._proposal.eligibility, Proposal.ELIGIBILITYNOTCHECKED)

        # Makes self._proposal not-eligible
        data = dict_to_multivalue_dict({'eligibility_decision_form-eligible': False,
                                        'eligibility_decision_form-comment': 'Not in the scope of the call',
                                        'save': 'Save Eligibility'
                                        })

        response = self._client_management.post(
            reverse('logged-proposal-eligibility-update', kwargs={'pk': self._proposal.id}),
            data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         reverse('logged-call-evaluation-proposal-detail', kwargs={'pk': self._proposal.id}))

        self._proposal.refresh_from_db()
        self.assertEqual(self._proposal.eligibility, Proposal.NOTELIGIBLE)
        self.assertEqual(self._proposal.eligibility_comment, 'Not in the scope of the call')

        # Makes self._proposal eligible
        data = dict_to_multivalue_dict({'eligibility_decision_form-eligible': True,
                                        'eligibility_decision_form-comment': 'Good proposal!',
                                        'save': 'Save Eligibility'
                                        })
        response = self._client_management.post(
            reverse('logged-proposal-eligibility-update', kwargs={'pk': self._proposal.id}),
            data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         reverse('logged-call-evaluation-proposal-detail', kwargs={'pk': self._proposal.id}))

        self._proposal.refresh_from_db()
        self.assertEqual(self._proposal.eligibility, Proposal.ELIGIBLE)
        self.assertEqual(self._proposal.eligibility_comment, 'Good proposal!')


class EvaluationCriteriaList(TestCase):
    def setUp(self):
        self._criterion = Criterion.objects.create(
            name='Feasibility', description='How feasible is the project'
        )
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(reverse('logged-evaluation_criteria-list'))
        self.assertContains(response, 'Feasibility')
        self.assertContains(response, 'How feasible is the project')


class EvaluationCriterionDetail(TestCase):
    def setUp(self):
        self._criterion = Criterion.objects.create(
            name='Feasibility', description='How feasible is the project'
        )
        self._client_management = database_population.create_management_logged_client()

    def test_get(self):
        response = self._client_management.get(
            reverse('logged-evaluation_criterion-detail', kwargs={'pk': self._criterion.pk}))
        self.assertContains(response, 'Feasibility')
        self.assertContains(response, 'How feasible is the project')
