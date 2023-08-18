from django.contrib import messages  # to delete
from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from web.forms import RegisterUserForm, MandateForm, ClientForm, EmployeeForm, ClientSingUpForm, EmployeeSingUpForm, \
    ContactPersonForm, AppUserForm
from web.models import Mandate, Client, AppUser, Employee, ContactPerson

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group


def index(request):
    clients = Client.objects.all()
    mandates = Mandate.objects.all()
    employees = Employee.objects.all()
    contact_person = ContactPerson.objects.all()
    context = {
        "clients": clients,
        "mandates": mandates,
        "employees": employees,
        "contact_person": contact_person,
    }
    return render(request, 'index.html', context=context)


def contact_us(request):
    return render(request, 'contact_us.html')


class AboutView(views.TemplateView):
    template_name = "about_us.html"


def employee_click_view(request):
    if request.user.is_authenticated:
        return redirect('after_login_view')
    return render(request, 'employee/employee_click.html')


def client_click_view(request):
    if request.user.is_authenticated:
        return redirect('after_login_view')
    return render(request, 'client/client_click.html')


# -------------------------- Login, Logout, Register Views ----------------------------------------------------

class EmployeeSignUpView(views.CreateView):
    model = AppUser
    form_class = EmployeeSingUpForm
    template_name = 'employee/register_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.all()
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


# def employee_register_view(request):
#     user_form = RegisterUserForm()
#     employee_form = EmployeeForm()
#
#     if request.method == 'POST':
#         user_form = RegisterUserForm(request.POST)
#         employee_form = EmployeeForm(request.POST, request.FILES)
#         if user_form.is_valid() and employee_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             employee = employee_form.save(commit=False)
#             employee.user = user
#             employee.save()
#             my_employee_group = Group.objects.get_or_create(name='EMPLOYEE')
#             my_employee_group[0].user_set.add(user)
#         return redirect('login_user')
#
#     context = {
#         'user_form': user_form,
#         'employee_form': employee_form
#     }
#
#     return render(request, 'employee/register_employee.html', context=context)


# def client_register_view(request):
#     if request.method == 'POST':
#         user_form = RegisterUserForm(request.POST)
#         contact_person_form = ContactPersonForm(request.POST, request.FILES)
#         if user_form.is_valid() and contact_person_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             contact_person = contact_person_form.save(commit=False)
#             contact_person.user = user
#             contact_person.save()
#             my_patient_group = Group.objects.get_or_create(name='CONTACT_PERSON')
#             my_patient_group[0].user_set.add(user)
#             return redirect('client_login')
#         else:
#             context = {'user_form': user_form, 'contact_person_form': contact_person_form}
#             return render(request, 'client/client_register.html', context=context)
#     user_form = RegisterUserForm()
#     contact_person_form = ContactPersonForm()
#     context = {'user_form': user_form, 'contact_person_form': contact_person_form}
#     return render(request, 'client/client_register.html', context=context)
class ContactPersonSingUpView(views.CreateView):
    model = AppUser
    form_class = ClientSingUpForm
    template_name = 'client/client_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class RegisterUserView(views.CreateView):
    template_name = 'app_auth/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class LogoutUserView(auth_views.LogoutView):
    pass


# -------------------------- End of Login, Logout, Register Views ----------------------------------------------------
def my_login_view(request):
    user = request.user

    if user.is_superuser:
        return redirect("admin_dashboard")
    elif user.is_staff and user.is_active:
        return redirect("employee_dashboard")
    # elif user.is_client:
    #     return redirect("client_dashboard")
    else:
        return redirect("login")


# -------------------------------- Admin Employees Views  ----------------------------------------------------
def admin_dashboard_view(request):
    clients = Client.objects.all()
    employees = Employee.objects.all().filter(user__is_active=False)
    employees_all = Employee.objects.all()
    mandates = Mandate.objects.all()
    contact_persons = ContactPerson.objects.all().filter(user__is_active=False)
    contact_persons_all = ContactPerson.objects.all()
    context = {
        'clients': clients,
        'mandates': mandates,
        'employees': employees,
        'contact_persons': contact_persons,
        'employees_all': employees_all,
        'contact_persons_all': contact_persons_all,

    }
    return render(request, 'admin_templates/admin_dashboard.html', context=context)


def admin_employee_view(request):
    return render(request, 'admin_templates/admin_employee.html')


class AdminEmployeeRecordsView(views.ListView):
    model = Employee
    template_name = 'admin_templates/admin_employee_records.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return self.model.objects.filter(user__is_active=True)


class EmployeeUpdateView(SuccessMessageMixin, views.UpdateView):
    model = Employee
    form_class = EmployeeForm
    # fields = "__all__"
    success_url = reverse_lazy('admin_employee_records')
    template_name = 'admin_templates/admin_update_employee.html'
    success_message = "Employee: %(first_name)s %(last_name)s updated successfully!"


class AdminApproveEmployeeView(views.ListView):
    template_name = 'admin_templates/admin_approve_employee.html'
    context_object_name = 'employees'
    queryset = Employee.objects.filter(user__is_active=False)


def admin_approve_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    user = AppUser.objects.get(pk=employee.user_id)
    user.is_active = True
    user.save()
    employee.save()
    messages.success(request, "Employee is approved successfully!")
    return redirect(reverse('admin_approve_employee_view'))


def admin_reject_employee_view(request, pk):
    employee = Employee.objects.get(id=pk)
    user = AppUser.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    messages.success(request, "Employee and User are deleted successfully!")
    return redirect('admin_approve_employee_view')


def admin_add_employee_view(request):
    user_form = RegisterUserForm()
    employee_form = EmployeeForm()

    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = True
            user.is_staff = True
            user.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

        return redirect('admin_employee')
    context = {
        "user_form": user_form,
        "employee_form": employee_form
    }
    return render(request, 'admin_templates/admin_create_employee.html', context=context)


def delete_employee_view(request, pk):
    employee = Employee.objects.get(id=pk)
    user = AppUser.objects.get(id=employee.user_id)
    user.delete()
    employee.delete()
    messages.success(request, "Employee and User are deleted successfully!")
    return redirect('admin_employee_records')


# -------------------------------- End Admin Employees Views  ----------------------------------------------------

# -------------------------------- Start Admin Client Views  ----------------------------------------------------
class AdminClientView(views.TemplateView):
    template_name = 'admin_templates/admin_client.html'


class AdminClientRecordsView(views.ListView):
    model = ContactPerson
    template_name = 'admin_templates/admin_client_records.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return self.model.objects.filter(user__is_active=True)


class AdminApproveClientView(views.ListView):
    template_name = 'admin_templates/admin_approve_client.html'
    context_object_name = 'clients'
    queryset = ContactPerson.objects.filter(user__is_active=False)


def admin_approve_client(request, pk):
    client = ContactPerson.objects.get(id=pk)
    user = AppUser.objects.get(id=client.user_id)
    user.is_active = True
    user.save()
    client.save()
    messages.success(request, "Client is approved successfully!")
    return redirect(reverse('admin_approve_client_view'))


def admin_reject_client_view(request, pk):
    client = ContactPerson.objects.get(id=pk)
    user = AppUser.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    messages.success(request, "Client and User are deleted successfully!")
    return redirect('admin_approve_client_view')


def admin_add_client_view(request):
    user_form = RegisterUserForm()
    client_form = ContactPersonForm()

    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        client_form = ContactPersonForm(request.POST, request.FILES)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = True
            user.is_active = True
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

        return redirect('admin_client')
    context = {
        "user_form": user_form,
        "client_form": client_form
    }
    return render(request, 'admin_templates/admin_create_client.html', context=context)


# class ContactPersonUpdateView(SuccessMessageMixin, views.UpdateView):
#     model = ContactPerson
#     form_class = ContactPersonForm
#     # fields = "__all__"
#     success_url = reverse_lazy('admin_client_records')
#     template_name = 'admin_templates/admin_update_client.html'
#     success_message = "Client: %(first_name)s %(last_name)s updated successfully!"


# class ContactPersonUpdateView(SuccessMessageMixin, views.UpdateView):
#     model = ContactPerson
#     template_name = 'admin_templates/admin_update_client.html'
#     form_class = ContactPersonForm
#     success_message = "Client: %(first_name)s %(last_name)s updated successfully!"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['app_user_form'] = RegisterUserForm(instance=self.object.user)
#         return context
#
#     def form_valid(self, form):
#         app_user_form = RegisterUserForm(self.request.POST, instance=self.object.user)
#         if app_user_form.is_valid():
#             app_user_form.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('admin_client_records')
def admin_update_contact_person(request, pk):
    contact_person = ContactPerson.objects.get(id=pk)
    user = AppUser.objects.get(id=contact_person.user_id)

    app_user_form = AppUserForm(instance=user)
    form = ContactPersonForm(request.FILES, instance=contact_person)
    if request.method == 'POST':
        app_user_form = AppUserForm(request.POST, instance=user)
        form = ContactPersonForm(request.POST, request.FILES, instance=contact_person)
        if app_user_form.is_valid() and form.is_valid():
            user = app_user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = form.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('admin_client_records')
    context = {'app_user_form': app_user_form, 'form': form}

    return render(request, 'admin_templates/admin_update_client.html', context=context)


def delete_client_view(request, pk):
    client = ContactPerson.objects.get(id=pk)
    user = AppUser.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    messages.success(request, "Employee and User are deleted successfully!")
    return redirect('admin_client_records')


# -------------------------------- End Admin Client Views  ------------------------------------------------------


class MandateListView(views.ListView):
    model = Mandate
    queryset = Mandate.objects.all()
    paginate_by = 5

    def get_queryset(self):
        object_list = self.model.objects.all()
        return object_list


# -------------------------- Mandate Views------------------------------------------------------------------------------
class MandateCreateView(SuccessMessageMixin, views.CreateView):
    model = Mandate
    form_class = MandateForm
    # fields = "__all__"
    success_url = reverse_lazy('mandate_list')
    # template_name = 'web/mandate_form.html'
    success_message = "Mandate: %(denotation)s created successfully!"


class MyLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_active:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class MandateListView(views.ListView):
    model = Mandate
    queryset = Mandate.objects.all()
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            object_list = self.model.objects.filter(Q(id__in=self.request.user.can_access) |
                                                    Q(denotation__icontains=q) | Q(priority__icontains=q) | Q(
                mandate_number__icontains=q)
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


# -------------------------- End of Mandate Views-----------------------------------------------------------------------


class ClientsCreateView(SuccessMessageMixin, views.CreateView):
    model = Client
    form_class = ClientForm
    # fields = "__all__"
    success_url = reverse_lazy('clients_list')
    template_name = 'web/client_form.html'
    success_message = "Mandate: %(denotation)s created successfully!"


class ClientsListView(LoginRequiredMixin, views.ListView):
    model = Client
    template_name = "web/clients_list.html"
    queryset = Client.objects.all()
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            object_list = self.model.objects.filter(
                Q(client_number__icontains=q) | Q(denotation__icontains=q)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


class ClientUpdateView(SuccessMessageMixin, views.UpdateView):
    model = Client
    form_class = ClientForm
    # fields = "__all__"
    success_url = reverse_lazy('clients_list')
    success_message = "Clients: %(denotation)s updated successfully!"


class ClientDeleteView(views.DeleteView):
    queryset = Client.objects.all()
    success_url = reverse_lazy('clients_list')

    def get_success_url(self):
        messages.success(self.request, "Client deleted successfully!")
        return reverse('clients_list')


# ----------- Check if Admin / Client / Employee Views ----------------------------------------------------------------
def is_admin_checker(user):
    return user.is_superuser


def is_employee_checker(user):
    return user.is_staff


# def is_client_checker(user):
#     return user.is_client

# TODO
def after_login_view(request):
    # if is_admin_checker(request.user):
    #     return redirect('admin_dashboard')
    # else:
    #     return redirect('admin_dashboard')

    if is_admin_checker(request.user):
        return redirect('admin_dashboard')
    elif is_employee_checker(request.user):
        account = Employee.objects.all().filter(user_id=request.user.id)
        if account:
            return redirect('employee_dashboard')
        else:
            return render(request, 'web/employee_wait_for_approval.html')
    # elif is_client_checker(request.user):
    #     account = ContactPerson.objects.all().filter(user_id=request.user.id, is_client=True)
    #     if account:
    #         return redirect('client-dashboard')
    #     else:
    #         return render(request, 'web/client_wait_for_approval.html')


# ----------- Check of Admin / Client / Employee Views ----------------------------------------------------------------


# def employee_update_view(request, pk):
#     employee = Employee.objects.get(pk=pk)
#     user = AppUser.objects.get(pk=employee.user_id)
#
#     user_form = RegisterUserForm(instance=user)
#     employee_form = EmployeeForm(request.FILES, instance=employee)
#
#     context = {
#         "user_form": user_form,
#         "employee_form": employee_form
#     }
#
#     if request.method == 'POST':
#         user_form = RegisterUserForm(request.POST, instance=user)
#         employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
#
#         if user_form.is_valid() and employee_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.is_active = True
#             user.save()
#             employee.save()
#
#         return redirect('admin_employee_records')
#     return render(request, 'admin_templates/admin_update_employee.html', context=context)
def employee_dashboard_view(request):
    clients = Client.objects.all()
    employees = Employee.objects.all().filter(user__is_active=False)
    employees_all = Employee.objects.all()
    mandates = Mandate.objects.all()
    contact_persons = ContactPerson.objects.all().filter(user__is_active=False)
    contact_persons_all = ContactPerson.objects.all()
    context = {
        'clients': clients,
        'mandates': mandates,
        'employees': employees,
        'contact_persons': contact_persons,
        'employees_all': employees_all,
        'contact_persons_all': contact_persons_all,

    }
    return render(request, 'employee/employee_dashboard.html', context=context)
