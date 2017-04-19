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
from django.conf.urls import url, include
from django.contrib import admin
from cms import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^plan_pdf/$', views.HomePDFView.as_view(), name='plan-pdf'),
    url(r'^admin/', admin.site.urls),
    url(r'^domaine/(?P<pk>\d+)$', views.DomaineDetailView.as_view(), name='domaine-detail'),
    url(r'^domaines/$', views.DomaineListView.as_view(), name='domaine-list'),
    url(r'^processus/(?P<pk>\d+)$', views.ProcessusDetailView.as_view(), name='processus-detail'),
    url(r'^processus/$', views.ProcessusListView.as_view(), name='processus-list'),
    url(r'^module/(?P<pk>\d+)$', views.ModuleDetailView.as_view(), name='module-detail'),
    url(r'^modules/$', views.ModuleListView.as_view(), name='module-list'),
    url(r'^periodes$', views.PeriodeView.as_view(), name='periodes'),
    url(r'^periodes_pdf$', views.PeriodePDFView.as_view(), name='periodes-pdf'),
    url(r'^evaluation/$', views.EvaluationView.as_view(), name='evaluation'),
    #url(r'^upload/$', views.AddDocument.as_view(), name='upload'), 
    #url(r'^download/(?P<file_name>.+)$', views.Download, name='download'),  
    #url(r'^calendrier/$', views.pdf_view, name='pdf-view'), 
    url(r'^module_pdf/(?P<pk>\d+)$', views.ModulePDF.as_view(), name='module-pdf'),
    url(r'^documents/$', views.DocumentListView.as_view(), name='document-list'), 
    url(r'^document/(?P<pk>\d+)$', views.DocumentDetailView.as_view(), name='document-detail'),
    url(r'^upload/(?P<pk>\d+)$', views.UploadDetailView.as_view(), name='upload-detail'), 
    url(r'^tinymce/', include('tinymce.urls'), name='tinymce-js'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
