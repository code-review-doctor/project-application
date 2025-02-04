from django.urls import path

import grant_management.views

urlpatterns = [
    path('logged/grant-management/project/list/',
         grant_management.views.ProjectList.as_view(),
         name='logged-grant_management-project-list'),
    path('logged/grant-management/project/<int:pk>/',
         grant_management.views.ProjectDetail.as_view(),
         name='logged-grant_management-project-detail'),

    path('logged/grant-management/project/<int:pk>/add-comment/',
         grant_management.views.ProjectDetailCommentAdd.as_view(),
         name='logged-grant_management-project-comment-add'),

    path('logged/grant-management/project/<int:pk>/update/',
         grant_management.views.ProjectUpdate.as_view(),
         name='logged-grant_management-project-update'),

    path('logged/grant-management/project/add/',
         grant_management.views.ProjectCreate.as_view(),
         name='logged-grant_management-project-add'),

    path('logged/grant-management/project/<int:project>/information/update/',
         grant_management.views.ProjectBasicInformationUpdateView.as_view(),
         name='logged-grant_management-project-basic-information-update'),
    path('logged/grant-management/project/<int:project>/lay_summaries/update/',
         grant_management.views.LaySummariesUpdateView.as_view(),
         name='logged-grant_management-lay_summaries-update'),
    path('logged/grant-management/project/<int:project>/blog_posts/update/',
         grant_management.views.BlogPostsUpdateView.as_view(),
         name='logged-grant_management-blog_posts-update'),
    path('logged/grant-management/project/<int:project>/scientific_reports/update/',
         grant_management.views.ScientificReportsUpdateView.as_view(),
         name='logged-grant_management-scientific_reports-update'),

    path('logged/grant-management/project/<int:project>/locations/update/',
         grant_management.views.LocationsUpdateView.as_view(),
         name='logged-grant_management-locations-update'),

    path('logged/grant-management/project/<int:project>/grant-agreement/add/',
         grant_management.views.GrantAgreementAddView.as_view(),
         name='logged-grant_management-grant_agreement-add'),
    path('logged/grant-management/grant-agreement/<int:pk>/update/',
         grant_management.views.GrantAgreementUpdateView.as_view(),
         name='logged-grant_management-grant_agreement-update'),
    path('logged/grant-management/grant-agreement/<int:pk>/add-comment/',
         grant_management.views.GrantAgreementCommentAdd.as_view(),
         name='logged-grant_management-grant_agreement-comment-add'),

    path('logged/grant-management/project/<int:project>/invoices/update/',
         grant_management.views.InvoicesUpdateView.as_view(),
         name='logged-grant_management-invoices-update'),

    path('logged/grant-management/project/<int:project>/financial_reports/update/',
         grant_management.views.FinancialReportsUpdateView.as_view(),
         name='logged-grant_management-financial_reports-update'),

    # path('logged/grant-management/project/<int:project>/finances/update/',
    #      grant_management.views.FinancesViewUpdate.as_view(),
    #      name='logged-grant_management-finances-update'),

    path('logged/grant-management/project/<int:project>/installments/update/',
         grant_management.views.InstallmentsUpdateView.as_view(),
         name='logged-grant_management-installments-update'),

    path('logged/grant-management/project/<int:project>/media/update/',
         grant_management.views.MediaUpdateView.as_view(),
         name='logged-grant_management-media-update'),

    path('logged/grant-management/project/<int:project>/data/update/',
         grant_management.views.DatasetUpdateView.as_view(),
         name='logged-grant_management-data-update'),

    path('logged/grant-management/project/<int:project>/publications/update/',
         grant_management.views.PublicationsUpdateView.as_view(),
         name='logged-grant_management-publications-update'),

    path('logged/grant-management/project/<int:project>/social_media/update/',
         grant_management.views.SocialMediaUpdateView.as_view(),
         name='logged-grant_management-social-media-update'),

    path('logged/grant-management/project/<int:project>/milestones/update/',
         grant_management.views.MilestoneUpdateView.as_view(),
         name='logged-grant_management-milestones-update'),

    path('logged/grant-management/project/<int:project>/close/',
         grant_management.views.CloseProjectView.as_view(),
         name='logged-grant_management-close_project'),

    path('lay-summaries/<int:call>/for_website/',
         grant_management.views.LaySummariesRaw.as_view(),
         name='lay-summaries-for_website'),

    path('logged/autocomplete/milestones-category-names/',
         grant_management.views.MilestoneCategoriesAutocomplete.as_view(create_field='name'),
         name='logged-grant_management-autocomplete-milestones-names'),

    path('api/media/list/', grant_management.views.ApiListMediaView.as_view(),
         name='api-list-media-view'),
    path('api/media/list/deleted/', grant_management.views.ApiListMediaDeletedView.as_view(),
         name='api-list-media-deleted-view'),
]
