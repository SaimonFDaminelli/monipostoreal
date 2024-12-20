from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Página Inicial
    path('', views.home, name='home'),
    
    # Indicadores
    path('add_indicador/', views.add_indicador, name='add_indicador'),
    path('indicador_save/', views.indicador_save, name='indicador_save'),
    path('indicadores/', views.indicadores_view, name='indicadores'),
    path('indicadores/delete/<int:id>/', views.indicador_delete, name='indicador_delete'),
    path('indicadores/update/<int:id>/', views.indicador_update, name='indicador_update'),


    # Metas
    path('metas/', views.metas_view, name='metas'),
    path('add_meta/', views.add_meta, name='add_meta'),
    path('metas_save/', views.metas_save, name='metas_save'),
    path('metas/delete/<int:id>/', views.metas_delete, name='metas_delete'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/export/', views.export_dashboard, name='export_dashboard'),

    # Administração
    path('admin/', views.admin_page, name='admin'),
    
    # Perfil do Usuário
    path('profile/', views.profile, name='profile'),
    
    # Relatório
    path('rel/', views.rel, name='rel'),
    
    # Autenticação
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
