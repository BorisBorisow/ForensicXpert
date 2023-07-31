from django.urls import path
from . import views

urlpatterns = (
    path('', views.index, name='index'),
    path('register/', views.RegisterUserView.as_view(), name='register_user'),
    path('login/', views.LoginUserView.as_view(), name='login_user'),
    path('after-login/', views.after_login_view, name='after_login_view'),
    path('logout/', views.LogoutUserView.as_view(), name='logout_user'),
    path('about/', views.AboutView.as_view(), name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('mandate/', views.MandateListView.as_view(), name='mandate_list'),
    path('create-mandate/', views.MandateCreateView.as_view(), name='create_mandate'),
    # path('create-mandate/', views.mandate_create, name='create_mandate'),
    path('update-mandate/<int:pk>/', views.MandateUpdateView.as_view(), name='update_mandate'),
    path('delete-mandate/<int:pk>/', views.MandateDeleteView.as_view(), name='delete_mandate'),

)
