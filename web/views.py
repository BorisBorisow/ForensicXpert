from django.contrib.auth import views as auth_views, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages  # to delete
from web.forms import RegisterUserForm, MandateForm
from web.models import Mandate, Client
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class RegisterUserView(views.CreateView):
    template_name = 'app_auth/register.html'
    form_class = RegisterUserForm

    # Static way of providing `success_url`
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class LogoutUserView(auth_views.LogoutView):
    pass


def index(request):
    clients = Client.objects.all()
    mandates = Mandate.objects.all()
    context = {
        "clients": clients,
        "mandates": mandates,
    }
    return render(request, 'index.html', context=context)


@login_required
def contact_us(request):
    return render(request, 'contact_us.html')


class AboutView(views.TemplateView):
    template_name = "about_us.html"


def admin_dashboard_view(request):
    clients = Client.objects.all()
    mandates = Mandate.objects.all()
    context = {
        'clients': clients,
        'mandates': mandates,

    }
    return render(request, 'admin_templates/admin_dashboard.html', context=context)


class MandateCreateView(SuccessMessageMixin, views.CreateView):
    model = Mandate
    form_class = MandateForm
    # fields = "__all__"
    success_url = reverse_lazy('mandate_list')
    # template_name = 'web/mandate_form.html'
    success_message = "Mandate: %(denotation)s created successfully!"


class MandateListView(LoginRequiredMixin, views.ListView):
    model = Mandate
    queryset = Mandate.objects.all()
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            object_list = self.model.objects.filter(
                Q(denotation__icontains=q) | Q(priority__icontains=q) | Q(mandate_number__icontains=q)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


class MandateUpdateView(SuccessMessageMixin, views.UpdateView):
    model = Mandate
    form_class = MandateForm
    # fields = "__all__"
    success_url = reverse_lazy('mandate_list')
    # template_name = 'web/mandate_form.html'
    success_message = "Mandate: %(denotation)s updated successfully!"


class MandateDeleteView(views.DeleteView):
    queryset = Mandate.objects.all()
    success_url = reverse_lazy('mandate_list')

    def get_success_url(self):
        messages.success(self.request, "Mandate deleted successfully!")
        return reverse('mandate_list')


