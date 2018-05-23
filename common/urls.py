"""eds URL Configuration

"""
import os
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from cms import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('plan_pdf/', views.print_plan_formation, name='plan-pdf'),
    path('admin/', admin.site.urls),
    path('domaine/<int:pk>/', views.DomaineDetailView.as_view(), name='domaine-detail'),
    path('domaines/', views.DomaineListView.as_view(), name='domaine-list'),
    path('processus/<int:pk>/', views.ProcessusDetailView.as_view(), name='processus-detail'),
    path('processus/', views.ProcessusListView.as_view(), name='processus-list'),
    path('module/<int:pk>/', views.ModuleDetailView.as_view(), name='module-detail'),
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('module_pdf/<int:pk>/', views.print_module_pdf, name='module-pdf'),
    path('periodes/', views.PeriodeView.as_view(), name='periodes'),
    path('periodes_pdf/', views.print_periode_formation, name='periodes-pdf'),
    path('competences/', views.CompetenceListView.as_view(), name='competences'),
    path('travail/', views.TravailPersoListView.as_view(), name='travail'),

    path('upload/', views.UploadDocListView.as_view(), name='uploaddoc-list'),
    path('concept/<int:pk>/', views.ConceptDetailView.as_view(), name='concept-detail'),
    path('tinymce/', include('tinymce.urls'), name='tinymce-js'),
    
    # Serve docs by Django to allow LoginRequiredMiddleware to apply
    path('media/doc/<path:path>', serve,
        {'document_root': os.path.join(settings.MEDIA_ROOT, 'doc'), 'show_indexes': False}
    ),
]
