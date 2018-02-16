"""eds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from cms import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # url(r'^plan_pdf/$', views.HomePDFView.as_view(), name='plan-pdf'),
    path('plan_pdf/', views.print_plan_formation, name='plan-pdf'),
    path('admin/', admin.site.urls),
    path('domaine/<int:pk>/', views.DomaineDetailView.as_view(), name='domaine-detail'),
    path('domaines/', views.DomaineListView.as_view(), name='domaine-list'),
    path('processus/<int:pk>/', views.ProcessusDetailView.as_view(), name='processus-detail'),
    path('processus/', views.ProcessusListView.as_view(), name='processus-list'),
    path('module/<int:pk>/', views.ModuleDetailView.as_view(), name='module-detail'),
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('periodes/', views.PeriodeView.as_view(), name='periodes'),
    path('periodes_pdf/', views.print_periode_formation, name='periodes-pdf'),
    path('evaluation/', views.EvaluationView.as_view(), name='evaluation'),
    path('competences/', views.CompetenceListView.as_view(), name='competences'),
    path('travail/', views.TravailPersoListView.as_view(), name='travail'),
    path('module_pdf/<int:pk>/', views.print_module_pdf, name='module-pdf'),
    path('upload/', views.UploadDocListView.as_view(), name='uploaddoc-list'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('upload/<int:pk>/', views.UploadDocDetailView.as_view(), name='uploaddoc-detail'),

    # url(r'^emplois/$', views.EmploiListView.as_view(), name='emploi-list'),
    path('tinymce/', include('tinymce.urls'), name='tinymce-js'),
    
    # Serve bulletins by Django to allow LoginRequiredMiddleware to apply
    path('media/doc/<path:path>', serve,
        {'document_root': os.path.join(settings.MEDIA_ROOT, 'doc'), 'show_indexes': False}
    ),
]
