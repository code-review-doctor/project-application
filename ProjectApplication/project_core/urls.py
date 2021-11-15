from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.defaults import server_error
from django.views.i18n import JavaScriptCatalog

import project_core.views.logged.proposals_export_to_csv_summary
import project_core.views.logged.proposals_export_to_excel
from .views import common
from .views import external
from .views import logged

urlpatterns = [
    path('',
         external.homepage.Homepage.as_view(),
         name='homepage'),
    path(f'{settings.ADMIN_URL}jsi18n/',
         JavaScriptCatalog.as_view(),
         name='javascript-jsi18n'),
    path('calls/',
         external.call.CallList.as_view(),
         name='call-list'),

    path('proposal/add/',
         external.proposal.ProposalView.as_view(),
         name='proposal-add'),
    path('proposal/<uuid:uuid>/update/',
         external.proposal.ProposalView.as_view(),
         name='proposal-update'),
    path('proposal/<uuid:uuid>/',
         external.proposal.ProposalDetailView.as_view(),
         name='proposal-detail'),
    path('proposal/thank-you/<uuid:uuid>/',
         external.proposal.ProposalThankYouView.as_view(),
         name='proposal-thank-you'),
    path('proposal/cannot-modify/',
         external.proposal.ProposalCannotModify.as_view(),
         name='proposal-cannot-modify'),
    path('proposal/question_answer/file/<int:proposal_qa_file_id>/<str:md5>/',
         common.proposal.ProposalQuestionAnswerFileView.as_view(),
         name='proposal-question-answer-file'),

    path('logged/proposals/',
         logged.proposal.ProposalList.as_view(),
         name='logged-proposal-list'),
    path('logged/proposal/preview/',
         logged.proposal.ProposalPreview.as_view(),
         name='logged-proposal-preview'),
    path('logged/proposal/<int:pk>/update/',
         logged.proposal.ProposalView.as_view(),
         name='logged-proposal-update'),
    path('logged/proposal/<int:pk>/',
         logged.proposal.ProposalDetailView.as_view(),
         name='logged-proposal-detail'),
    path('logged/proposal/<int:pk>/comment/add/',
         logged.proposal.ProposalCommentAdd.as_view(),
         name='logged-proposal-comment-add'),
    path('logged/proposals/export/excel/<int:call>/',
         project_core.views.logged.proposals_export_to_excel.ProposalsExportExcel.as_view(),
         name='logged-export-proposals-for-call-excel'),
    path('logged/proposals/export/csv/summary/<int:call>/',
         project_core.views.logged.proposals_export_to_csv_summary.ProposalsExportCsvSummary.as_view(),
         name='logged-export-proposals-csv-summary-call'),
    path('logged/proposals/export/csv/summary/',
         project_core.views.logged.proposals_export_to_csv_summary.ProposalsExportCsvSummary.as_view(),
         name='logged-export-proposals-csv-summary-all'),

    path('logged/call/list/',
         logged.call.CallList.as_view(),
         name='logged-call-list'),
    path('logged/call/add/',
         logged.call.CallView.as_view(),
         name='logged-call-add'),
    path('logged/call/<int:pk>/update/',
         logged.call.CallView.as_view(),
         name='logged-call-update'),
    path('logged/call/<int:call_id>/list_proposals/',
         logged.call.ProposalList.as_view(),
         name='logged-call-list-proposals'),
    path('logged/call/proposal/<int:pk>/',
         logged.call.ProposalDetail.as_view(),
         name='logged-call-proposal-detail'),
    path('logged/call/<int:pk>/comment/add/',
         logged.call.CallCommentAdd.as_view(),
         name='logged-call-comment-add'),
    path('logged/call/<int:pk>/',
         logged.call.CallDetailView.as_view(),
         name='logged-call-detail'),
    path('logged/calls/',
         logged.call.CallList.as_view(),
         name='logged-calls'),

    # Call Parts
    path('logged/call/<int:call_pk>/parts/list/',
         logged.call_part.CallPartList.as_view(),
         name='logged-call-part-list'),
    path('logged/call/<int:call_pk>/parts/add/',
         logged.call_part.CallPartCreate.as_view(),
         name='logged-call-part-add'),
    path('logged/call/<int:call_pk>/parts/<int:call_part_pk>/update/',
         logged.call_part.CallPartUpdate.as_view(),
         name='logged-call-part-update'),
    path('logged/call/<int:call_pk>/parts/<int:call_part_pk>/',
         logged.call_part.CallPartDetail.as_view(),
         name='logged-call-part-detail'),
    path('logged/call/call_part/delete/',
         logged.call_part.CallPartDelete.as_view(),
         name='logged-call-part-delete'),

    # Call (part) Files
    path('logged/call/<int:call_pk>/file/<int:call_file_pk>/',
         logged.call_part_file.CallFileView.as_view(),
         name='logged-call-part-file-detail'),
    path('logged/call/<int:call_pk>/part/<int:call_part_pk>/file/list',
         logged.call_part_file.CallPartFileList.as_view(),
         name='logged-call-part-file-list'),
    path('logged/call/<int:call_pk>/file/<int:call_file_pk>/update/',
         logged.call_part_file.CallPartFileUpdate.as_view(),
         name='logged-call-part-file-update'),
    path('logged/call/<int:call_pk>/call_part/<int:call_part_pk>/file/add/',
         logged.call_part_file.CallPartFileCreate.as_view(),
         name='logged-call-part-file-add'),
    path('logged/call/call_part/file/delete/',
         logged.call_part_file.CallPartFileDelete.as_view(),
         name='logged-call-part-file-delete'),

    # Call (part) Questions
    path('logged/call/<int:call_pk>/question/<int:call_question_pk>/',
         logged.call_question.CallPartQuestionView.as_view(),
         name='logged-call-part-question-detail'),
    path('logged/call/<int:call_pk>/question/<int:call_question_pk>/update/',
         logged.call_question.CallPartQuestionUpdate.as_view(),
         name='logged-call-part-question-update'),
    path('logged/call/<int:call_pk>/question/<int:call_part_pk>/add/',
         logged.call_question.CallPartQuestionTemplateQuestionUpdate.as_view(),
         name='logged-call-part-question-add'),

    path('logged/',
         logged.homepage.Homepage.as_view(),
         name='logged-homepage'),
    path('logged/news/',
         logged.news.News.as_view(),
         name='logged-news'),

    path('logged/home/changelog/',
         logged.changelog.Changelog.as_view(),
         name='logged-changelog'),

    path('logged/template_question/add/',
         logged.template_question.TemplateQuestionCreateView.as_view(),
         name='logged-template-question-add'),
    path('logged/template_question/<int:pk>/',
         logged.template_question.TemplateQuestionDetailView.as_view(),
         name='logged-template-question-detail'),
    path('logged/template_question/<int:pk>/update/',
         logged.template_question.TemplateQuestionUpdateView.as_view(),
         name='logged-template-question-update'),
    path('logged/template_questions/',
         logged.template_question.TemplateQuestionList.as_view(),
         name='logged-template-question-list'),

    path('logged/funding_instrument/add/',
         logged.funding_instrument.FundingInstrumentView.as_view(),
         name='logged-funding-instrument-add'),
    path('logged/funding_instrument/<int:pk>/',
         logged.funding_instrument.FundingInstrumentDetailView.as_view(),
         name='logged-funding-instrument-detail'),
    path('logged/funding_instrument/<int:pk>/update/',
         logged.funding_instrument.FundingInstrumentView.as_view(),
         name='logged-funding-instrument-update'),
    path('logged/funding_instruments/',
         logged.funding_instrument.FundingInstrumentList.as_view(),
         name='logged-funding-instrument-list'),

    path('logged/person_position/add/',
         logged.person_position.PersonPositionCreateView.as_view(),
         name='logged-person-position-add'),
    path('logged/person_position/<int:pk>/',
         logged.person_position.PersonPositionDetailView.as_view(),
         name='logged-person-position-detail'),
    path('logged/person_position/<int:pk>/update/',
         logged.person_position.PersonPositionUpdateView.as_view(),
         name='logged-person-position-update'),
    path('logged/person_position/',
         logged.person_position.PersonPositionListView.as_view(),
         name='logged-person-position-list'),

    path('logged/lists/',
         logged.lists.ListsView.as_view(),
         name='logged-lists'),

    path('logged/project/list/',
         logged.project.ProjectList.as_view(),
         name='logged-project-list'),
    path('logged/project/<int:pk>/',
         logged.project.ProjectDetailView.as_view(),
         name='logged-project-detail'),
    path('logged/project/<int:pk>/comment/add/',
         logged.project.ProjectCommentAdd.as_view(),
         name='logged-project-comment-add'),

    path('logged/financial_keys/list/',
         logged.project.FinancialKeyListView.as_view(),
         name='logged-financial-key-list'),

    path('logged/financial_keys/add/',
         logged.project.FinancialKeyAdd.as_view(),
         name='logged-financial-key-update'),

    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='registration/login.tmpl',
                                      extra_context={'contact': settings.LOGIN_CONTACT}),
         name='accounts-login'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('autocomplete/organisations/',
         common.autocomplete.OrganisationsAutocomplete.as_view(create_field='name'),
         name='autocomplete-organisation-names'),
    path('autocomplete/keywords/',
         common.autocomplete.KeywordsAutocomplete.as_view(create_field='name'),
         name='autocomplete-keywords'),
    path('logged/autocomplete/physical_people/',
         logged.autocomplete.PhysicalPersonAutocomplete.as_view(),
         name='logged-autocomplete-physical-people'),
    path('logged/autocomplete/person_positions/',
         logged.autocomplete.PersonPositionsAutocomplete.as_view(),
         name='logged-autocomplete-person-positions'),

    path('raises500/', server_error),
]
