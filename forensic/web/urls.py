from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = (
    path('', views.index, name='index'),

    path('employee-click/', views.employee_click_view, name='employee_click'),
    path('client-click/', views.client_click_view, name='client_click'),

    path('register/', views.RegisterUserView.as_view(), name='register_user'),
    # path('admin-register/', views.AdminRegisterView.as_view(), name='register_admin'),
    # path('employee-register/', views.employee_register_view, name='register_employee'),
    path('employee-register/', views.EmployeeSignUpView.as_view(), name='register_employee'),
    path('client-register/', views.ContactPersonSingUpView.as_view(), name='register_client'),

    path('employee-login/', LoginView.as_view(template_name='employee/employee_login.html'), name="employee_login"),
    path('client-login/', LoginView.as_view(template_name='client/client_login.html'), name="client_login"),
    # path('login/', views.LoginUserView.as_view(), name='login_user'),
    path('after-login/', views.after_login_view, name='after_login_view'),

    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    path('admin-employee/', views.admin_employee_view, name='admin_employee'),
    path('admin-employee-records/', views.AdminEmployeeRecordsView.as_view(), name='admin_employee_records'),
    path('admin-employee-records/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='admin_update_employee'),
    path('admin-employee/approve/', views.AdminApproveEmployeeView.as_view(), name='admin_approve_employee_view'),
    path('admin-employee-approve/approve/<int:pk>', views.admin_approve_employee, name='admin_approve_employee'),
    path('admin-employee-approve/reject/<int:pk>/', views.admin_reject_employee_view, name='reject_employee'),
    path('admin-employee-records/delete/<int:pk>/', views.delete_employee_view, name='delete_employee'),
    path('admin-add-employee/', views.admin_add_employee_view, name='admin_add_employee'),

    path('admin-client/', views.AdminClientView.as_view(), name='admin_client'),
    path('admin-client-records/', views.AdminClientRecordsView.as_view(), name='admin_client_records'),
    path('admin-client-records/update/<int:pk>/', views.admin_update_contact_person, name='admin_update_client'),
    path('admin-client/approve/', views.AdminApproveClientView.as_view(), name='admin_approve_client_view'),
    path('admin-client-approve/approve/<int:pk>', views.admin_approve_client, name='admin_approve_client'),
    path('admin-client-approve/reject/<int:pk>/', views.admin_reject_client_view, name='admin_reject_client'),
    path('admin-client-records/delete/<int:pk>/', views.delete_client_view, name='admin_delete_client'),
    path('admin-add-client/', views.admin_add_client_view, name='admin_add_client'),

    # ------------------------   END Admin URLS ------------------

    path('employee-dashboard/', views.employee_dashboard_view, name='employee_dashboard'),

    path('login/', views.LoginUserView.as_view(), name='login_user'),
    path('after-login/', views.after_login_view, name='after_login_view'),
    path('logout/', views.LogoutUserView.as_view(), name='logout_user'),
    path('about/', views.AboutView.as_view(), name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),

    path('mandate/', views.MandateListView.as_view(), name='mandate_list'),
    path('create-mandate/', views.MandateCreateView.as_view(), name='create_mandate'),
    path('update-mandate/<int:pk>/', views.MandateUpdateView.as_view(), name='update_mandate'),
    path('delete-mandate/<int:pk>/', views.MandateDeleteView.as_view(), name='delete_mandate'),

    path('clients/', views.ClientsListView.as_view(), name='clients_list'),
    path('clients/create/', views.ClientsCreateView.as_view(), name='create_client'),
    path('update-client/<int:pk>/', views.ClientUpdateView.as_view(), name='update_client'),
    path('delete-client/<int:pk>/', views.ClientDeleteView.as_view(), name='delete_client'),
)
