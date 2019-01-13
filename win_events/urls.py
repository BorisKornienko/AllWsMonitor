from django.urls import path

from . import views

app_name = 'win_events'
urlpatterns = [
    path('powerbi_csv/sys/', views.raw_csv_sys, name='powerbi_csv_sys'),
    path('powerbi_csv/app/', views.raw_csv_app, name='powerbi_csv_app'),
    path('powerbi_csv/app2w/', views.raw_csv_app_2w, name='powerbi_csv_app_2w'),
    path('powerbi_csv/sys2w/', views.raw_csv_sys_2w, name='powerbi_csv_sys_2w'),
    path('powerbi_csv/sys2w-sc/', views.raw_csv_sys_2w_scales, name='powerbi_csv_sys_2w_sc'),
    path('powerbi_csv/app2w-sc/', views.raw_csv_app_2w_scales, name='powerbi_csv_app_2w_sc'),
    path('', views.IndexView.as_view(), name='index')
]