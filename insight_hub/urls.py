from django.urls import path
from .views import views, accounts,api_accounts,api_views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',accounts.register_page,name="register"),
    path('login/',accounts.login_page,name="login"),
    path("logout/",accounts.logout, name="logout"),
    path('dashboard/<uuid:id>/', views.dashboard, name='dashboard'),
    path('delete_dashboard/<uuid:id>/', views.delete_dashboard, name='delete_dashboard'),
    path("update_dashboard/<uuid:id>/",views.update_dashboard,name="update_dashboard"),
    path("create_chart/<uuid:id>/",views.create_chart,name="create_chart"),
    path("update_chart/<uuid:id>/",views.update_chart,name="update_chart"),
    path("delete_chart/<int:id>/",views.delete_chart,name="delete_chart"),

    path("api/like_dashboard/",api_views.like_dashboard,name="like_dashboard"),
    path("api/register/", api_accounts.register_api, name="register_api"),
    path("api/login/",api_accounts.login_api,name="login_api"),
    path("api/upload_csv/",api_views.upload_csv,name="upload_csv"),
    path("api/create_dashboard/",api_views.create_dashboard,name="create_dashboard"),


]