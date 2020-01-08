import textwrap

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import TemplateView

from project_core.models import Proposal
from project_core.views.common.proposal import AbstractProposalDetailView, AbstractProposalView


def send_email_proposal_received(uuid, request):
    proposal = Proposal.objects.get(uuid=uuid)

    if not proposal.draft_saved_mail_sent or not proposal.submitted_mail_sent:
        recipient_list = [proposal.applicant.main_email()]

        footer = textwrap.dedent('''\
            Thank you for submitting your proposal. The SPI team remains at your disposal for questions at spi-grants@epfl.ch
            Please note that this email is sent from a non-monitored email address.
            ''')

        if proposal.status_is_draft() and not proposal.draft_saved_mail_sent:
            edit_url = request.build_absolute_uri(reverse('proposal-update', kwargs={'uuid': uuid}))
            call_deadline = proposal.call.submission_deadline.strftime('%A %d %B %Y at %H:%M Swiss time')

            subject = 'Swiss Polar Institute - Proposal draft saved'
            body = textwrap.dedent(f'''\
                Your proposal: {proposal.title} for the call {proposal.call.long_name} is saved.
                
                To Edit it go to: {edit_url}
                
                Please remember to submit it before the Call deadline: {call_deadline}.
                
                {footer}
                ''')

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
            proposal.draft_saved_mail_sent = True
            proposal.save()

        if proposal.status_is_submitted() and not proposal.submitted_mail_sent:
            subject = 'Swiss Polar Institute - Proposal submitted'
            view_url = request.build_absolute_uri(reverse('proposal-detail', kwargs={'uuid': uuid}))
            body = textwrap.dedent(f'''\
                Thanks for submitting your proposal: {proposal.title} for the call {proposal.call.long_name}
                
                You can see it on: {view_url}
                
                We will get in touch soon.
                
                {footer}''')

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
            proposal.submitted_mail_sent = True
            proposal.save()


class ProposalThankYouView(TemplateView):
    template_name = 'external/proposal-thank_you.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['proposal'] = Proposal.objects.get(uuid=kwargs['uuid'])

        send_email_proposal_received(kwargs['uuid'], self.request)

        return context


class ProposalCannotModify(TemplateView):
    template_name = 'external/proposal-cannot_modify.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProposalDetailView(AbstractProposalDetailView):
    template = 'external/proposal-detail.tmpl'


class ProposalView(AbstractProposalView):
    created_or_updated_url = 'proposal-thank-you'
    form_template = 'common/proposal-form.tmpl'
    action_url_update = 'proposal-update'
    action_url_add = 'proposal-add'
