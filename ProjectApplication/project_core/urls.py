from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

import project_core.views.autocomplete
from .views import external
from .views import management
from .views import internal


urlpatterns = [
    path('', external.Homepage.as_view(), name='homepage'),
    path('admin/jsi18n/', JavaScriptCatalog.as_view(), name='javascript-jsi18n'),
    path('calls/', external.CallsList.as_view(), name='calls-list'),
    path('proposal/add/', external.ProposalView.as_view(), name='proposal-add'),
    path('proposal/<uuid:uuid>/update', external.ProposalView.as_view(), name='proposal-update'),
    path('proposal/<uuid:uuid>/', external.ProposalDetailView.as_view(), name='proposal-detail'),
    path('proposal/thank-you/<uuid:uuid>/', external.ProposalThankYouView.as_view(), name='proposal-thank-you'),
    path('proposal/too-late/', external.ProposalTooLate.as_view(), name='proposal-too-late'),

    path('management/proposals', management.ProposalsList.as_view(), name='management-proposals-list'),
    path('management/proposal/<uuid:uuid>/update', management.ProposalView.as_view(),
         name='management-proposal-update'),
    path('management/proposal/<uuid:uuid>/', management.ProposalDetailView.as_view(),
         name='management-proposal-detail'),
    path('management/proposals/export/excel/<int:call>/', internal.proposal.ProposalsExportExcel.as_view(),
         name='management-export-proposals-for-call-excel'),
    path('management/proposals/export/excel/', internal.proposal.ProposalsExportExcel.as_view(),
         name='management-export-proposals-all-calls-excel'),

    path('management/call/list', management.CallsList.as_view(), name='management-calls-list'),
    path('management/call/add/', management.CallView.as_view(), name='call-add'),
    path('management/call/<int:id>/update', management.CallView.as_view(), name='management-call-update'),
    path('management/call/<int:id>/', management.CallDetailView.as_view(), name='management-call-detail'),
    path('management/calls/', management.CallsList.as_view(), name='management-calls'),
    path('management/', management.Homepage.as_view(), name='management-homepage'),

    path('management/templatequestion/add', management.TemplateQuestionCreateView.as_view(),
         name='template-question-add'),
    path('management/templatequestion/<int:pk>/', management.TemplateQuestionDetailView.as_view(),
         name='template-question-detail'),
    path('management/templatequestion/<int:pk>/update', management.TemplateQuestionUpdateView.as_view(),
         name='template-question-update'),
    path('management/templatequestions/', management.QuestionsList.as_view(), name='template-questions-list'),

    path('management/contact/add', management.ContactsCreateView.as_view(), name='management-contact-add'),
    path('management/contact/<int:pk>/', management.ContactDetailView.as_view(), name='contact-detail'),
    path('management/contact/<int:pk>/update', management.ContactUpdateView.as_view(), name='contact-update'),
    path('management/contacts/', management.ContactsListView.as_view(), name='management-contacts-list'),

    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='registration/login.tmpl',
                                      extra_context={'contact': settings.LOGIN_CONTACT,
                                                     'demo_management_user': settings.DEMO_MANAGEMENT_USER,
                                                     'demo_management_password': settings.DEMO_MANAGEMENT_PASSWORD})),
    path('accounts/', include('django.contrib.auth.urls')),

    path('autocomplete/organisations/', project_core.views.autocomplete.OrganisationsAutocomplete.as_view(),
         name='autocomplete-organisations'),
    path('autocomplete/keywords/', project_core.views.autocomplete.KeywordsAutocomplete.as_view(create_field='name'),
         name='autocomplete-keywords')
]
