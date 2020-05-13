from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView

from grant_management.forms.blog_posts import BlogPostsFormSet, BlogPostsInlineFormSet
from grant_management.forms.grant_agreement import GrantAgreementForm
from grant_management.forms.installments import InstallmentsFormSet, InstallmentsInlineFormSet
from grant_management.forms.invoices import InvoicesInlineFormSet, InvoicesFormSet
from grant_management.forms.lay_summaries import LaySummariesFormSet, LaySummariesInlineFormSet
from grant_management.forms.project_basic_information import ProjectBasicInformationForm
from grant_management.forms.reports import FinancialReportsInlineFormSet, ScientificReportsInlineFormSet, ReportsFormSet
from grant_management.models import GrantAgreement
from project_core.models import Project
from .forms.dataset import DatasetsFormSet, DatasetInlineFormSet
from .forms.media import MediaInlineFormSet, MediaFormSet
from .forms.project import ProjectForm


class ProjectList(TemplateView):
    template_name = 'grant_management/project-list.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['projects_active'] = Project.objects.all().filter(status=Project.ONGOING)
        context['projects_inactive'] = Project.objects.all().exclude(status=Project.ONGOING)

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'
                        })

        context['breadcrumb'] = [{'name': 'Grant management'}]

        return context


class ProjectDetail(DetailView):
    template_name = 'grant_management/project-detail.tmpl'
    context_object_name = 'project'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = context['project']

        if hasattr(project, 'grantagreement'):
            context['grant_agreement_button_text'] = 'Edit'
            context['grant_agreement_button_url'] = reverse('logged-grant_management-grant_agreement-update',
                                                            kwargs={'pk': project.grantagreement.id})
        else:
            context['grant_agreement_button_text'] = 'Create'
            context['grant_agreement_button_url'] = reverse('logged-grant_management-grant_agreement-add',
                                                            kwargs={'project': project.id})

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                                 {'name': f'Project detail ({project.key_pi()})'}]

        context['lay_summaries_count'] = project.laysummary_set.exclude(text='').count()
        context['blog_posts_count'] = project.blogpost_set.exclude(text='').count()

        return context


class ProjectUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'grant_management/project-form.tmpl'
    form_class = ProjectForm
    model = Project
    success_message = 'Project updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'active_section': 'lists',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'logged/_sidebar-lists.tmpl'})

        context['breadcrumb'] = [{'name': 'Lists', 'url': reverse('logged-lists')},
                                 {'name': 'Projects', 'url': reverse('logged-project-list')},
                                 {'name': f'Project update ({context["object"].key_pi()})'}]

        return context

    def get_success_url(self):
        return reverse('logged-project-detail', kwargs={'pk': self.object.pk})


class ProjectBasicInformationUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'grant_management/project-basic_information-form.tmpl'
    form_class = ProjectBasicInformationForm
    model = Project
    success_message = 'Project information updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.get(id=self.kwargs['pk'])

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                                 {'name': f'Project detail ({project.key_pi()})',
                                  'url': reverse('logged-grant_management-project-detail', kwargs={'pk': project.id})},
                                 {'name': 'Project basic information Edit'}]

        context['project'] = project
        return context

    def get_success_url(self):
        return reverse('logged-grant_management-project-detail', kwargs={'pk': self.object.pk})


def context_data_grant_greement(project):
    context = {'active_section': 'grant_management',
               'active_subsection': 'project-list',
               'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'}

    context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                             {'name': f'Project detail ({project.key_pi()})',
                              'url': reverse('logged-grant_management-project-detail', kwargs={'pk': project.id})},
                             {'name': 'Grant agreement'}]

    context['project'] = project

    return context


class GrantAgreementAddView(SuccessMessageMixin, CreateView):
    template_name = 'grant_management/grant_agreement-form.tmpl'
    form_class = GrantAgreementForm
    model = GrantAgreement
    success_message = 'Grant agreement added'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.get(id=self.kwargs['project'])

        context.update(context_data_grant_greement(project))

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = Project.objects.get(id=self.kwargs['project'])
        return kwargs

    def get_success_url(self):
        return reverse('logged-grant_management-project-detail', kwargs={'pk': self.object.project.pk})


class GrantAgreementUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'grant_management/grant_agreement-form.tmpl'
    form_class = GrantAgreementForm
    model = GrantAgreement
    success_message = 'Grant agreement updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = context['grantagreement'].project

        context.update(context_data_grant_greement(project))

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = kwargs['instance'].project
        return kwargs

    def get_success_url(self):
        return reverse('logged-grant_management-project-detail', kwargs={'pk': self.object.project.pk})


def grant_management_project_url(kwargs):
    return reverse('logged-grant_management-project-detail', kwargs={'pk': kwargs['project']})


class BlogPostsUpdateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = grant_management_project_url(kwargs)

        project = Project.objects.get(id=kwargs['project'])

        context['project'] = project

        context[BlogPostsFormSet.FORM_NAME] = BlogPostsInlineFormSet(prefix=BlogPostsFormSet.FORM_NAME,
                                                                     instance=project)

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                                 {'name': f'Project detail ({project.key_pi()})',
                                  'url': reverse('logged-grant_management-project-detail', kwargs={'pk': project.id})},
                                 {'name': 'Blog Posts'}]

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context[BlogPostsFormSet.FORM_NAME] = BlogPostsInlineFormSet(prefix=BlogPostsFormSet.FORM_NAME,
                                                                     instance=context['project'])

        return render(request, 'grant_management/blog_posts-form.tmpl', context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        blog_posts_form = BlogPostsInlineFormSet(request.POST, request.FILES,
                                                 prefix=BlogPostsFormSet.FORM_NAME,
                                                 instance=context['project'])

        if blog_posts_form.is_valid():
            blog_posts_form.save()
            messages.success(request, 'Blog posts saved')
            return redirect(grant_management_project_url(kwargs))

        messages.error(request, 'Blog posts not saved. Verify errors in the form')

        context[BlogPostsFormSet.FORM_NAME] = blog_posts_form

        return render(request, 'grant_management/blog_posts-form.tmpl', context)


class LaySummariesUpdateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = grant_management_project_url(kwargs)

        project = Project.objects.get(id=kwargs['project'])

        context['project'] = project

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                                 {'name': f'Project detail ({project.key_pi()})',
                                  'url': reverse('logged-grant_management-project-detail', kwargs={'pk': project.id})},
                                 {'name': 'Lay Summaries'}]

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context[LaySummariesFormSet.FORM_NAME] = LaySummariesInlineFormSet(prefix=LaySummariesFormSet.FORM_NAME,
                                                                           instance=context['project'])

        return render(request, 'grant_management/lay_summaries-form.tmpl', context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        lay_summaries_form = LaySummariesInlineFormSet(request.POST, request.FILES,
                                                       prefix=LaySummariesFormSet.FORM_NAME,
                                                       instance=context['project'])

        if lay_summaries_form.is_valid():
            lay_summaries_form.save()
            messages.success(request, 'Lay summaries saved')
            return redirect(grant_management_project_url(kwargs))

        messages.error(request, 'Lay summaries not saved. Verify errors in the form')

        context[LaySummariesFormSet.FORM_NAME] = lay_summaries_form

        return render(request, 'grant_management/lay_summaries-form.tmpl', context)


class UpdateView(TemplateView):
    def __init__(self, *args, **kwargs):
        self._breadcrumb_name = kwargs.pop('breadcrumb_name')
        self._formset_name = kwargs.pop('formset_name')
        self._inline_formset = kwargs.pop('inline_formset')
        self.template_name = kwargs.pop('template_name')
        self._human_type = kwargs.pop('human_type')

        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = grant_management_project_url(kwargs)

        project = Project.objects.get(id=kwargs['project'])

        context['project'] = project

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [
            {'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
            {'name': f'Project detail ({project.key_pi()})',
             'url': reverse('logged-grant_management-project-detail', kwargs={'pk': project.id})},
            {'name': self._breadcrumb_name}]

        context[self._formset_name] = self._inline_formset(prefix=self._formset_name, instance=context['project'])

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        forms = self._inline_formset(request.POST, request.FILES, prefix=self._formset_name,
                                     instance=context['project'])

        if forms.is_valid():
            forms.save()
            messages.success(request, f'{self._human_type} saved')
            return redirect(grant_management_project_url(kwargs))

        messages.error(request, f'{self._human_type} not saved. Verify errors in the form')

        context[self._formset_name] = forms

        return render(request, self.template_name, context)


class DatasetUpdateView(UpdateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         breadcrumb_name='Data',
                         formset_name=DatasetsFormSet.FORM_NAME,
                         inline_formset=DatasetInlineFormSet,
                         template_name='grant_management/dataset-form.tmpl',
                         human_type='Data'
                         )


class MediaUpdateView(UpdateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         breadcrumb_name='Media',
                         formset_name=MediaFormSet.FORM_NAME,
                         inline_formset=MediaInlineFormSet,
                         template_name='grant_management/media-form.tmpl',
                         human_type='Media'
                         )


class InstallmentsUpdateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cancel_url'] = grant_management_project_url(kwargs)

        project = Project.objects.get(id=kwargs['project'])

        context['project'] = project

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                                 {'name': f'Project detail ({project.key_pi()})',
                                  'url': reverse('logged-grant_management-project-detail', kwargs={'pk': project.id})},
                                 {'name': 'Installments'}]

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context[InstallmentsFormSet.FORM_NAME] = InstallmentsInlineFormSet(
            prefix=InstallmentsFormSet.FORM_NAME,
            instance=context['project'])

        return render(request, 'grant_management/installments-form.tmpl', context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        installments_form = InstallmentsInlineFormSet(request.POST, request.FILES,
                                                      prefix=InstallmentsFormSet.FORM_NAME,
                                                      instance=context['project'])

        if installments_form.is_valid():
            installments_form.save()
            messages.success(request, 'Installments saved')
            return redirect(grant_management_project_url(kwargs))

        messages.error(request, 'Installments not saved. Verify errors in the form')

        context[InstallmentsFormSet.FORM_NAME] = installments_form

        return render(request, 'grant_management/installments-form.tmpl', context)


class ScientificReportsUpdateView(UpdateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         breadcrumb_name='Scientific reports',
                         formset_name=ReportsFormSet.FORM_NAME,
                         inline_formset=ScientificReportsInlineFormSet,
                         template_name='grant_management/scientific_reports-form.tmpl',
                         human_type='Scientific reports'
                         )


class FinancesViewUpdate(TemplateView):
    FORM_NAME = 'financial_reports_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.get(id=kwargs['project'])

        context['project'] = project

        context['cancel_url'] = grant_management_project_url(kwargs)

        context.update({'active_section': 'grant_management',
                        'active_subsection': 'project-list',
                        'sidebar_template': 'grant_management/_sidebar-grant_management.tmpl'})

        context['breadcrumb'] = [{'name': 'Grant management', 'url': reverse('logged-grant_management-project-list')},
                                 {'name': f'Project detail ({project.key_pi()})',
                                  'url': reverse('logged-grant_management-project-detail',
                                                 kwargs={'pk': project.id})},
                                 {'name': 'Finances'}]

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context[InvoicesFormSet.FORM_NAME] = InvoicesInlineFormSet(prefix=InvoicesFormSet.FORM_NAME,
                                                                   instance=context['project'])
        context[FinancesViewUpdate.FORM_NAME] = FinancialReportsInlineFormSet(
            prefix='financial_reports_form', instance=context['project'])

        return render(request, 'grant_management/finances-form.tmpl', context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        invoices_form = InvoicesInlineFormSet(request.POST, request.FILES,
                                              prefix=InvoicesFormSet.FORM_NAME,
                                              instance=context['project'],
                                              form_kwargs={'user': request.user})

        financial_reports_form = FinancialReportsInlineFormSet(request.POST, request.FILES,
                                                               prefix='financial_reports_form',
                                                               instance=context['project'],
                                                               form_kwargs={'user': request.user})

        if all([invoices_form.is_valid(), financial_reports_form.is_valid()]):
            invoices_form.save()
            financial_reports_form.save()
            messages.success(request, 'Finance details saved')
            return redirect(reverse('logged-grant_management-project-detail', kwargs={'pk': context['project'].id}))

        messages.error(request, 'Finance details not saved. Verify errors in the forms')

        context[InvoicesFormSet.FORM_NAME] = invoices_form
        context[FinancesViewUpdate.FORM_NAME] = financial_reports_form

        return render(request, 'grant_management/finances-form.tmpl', context)


class LaySummariesRaw(TemplateView):
    template_name = 'grant_management/lay_summaries-raw.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        call_id = kwargs['call']

        projects = Project.objects.filter(call_id=call_id).order_by('key')

        context['projects'] = projects

        return context
