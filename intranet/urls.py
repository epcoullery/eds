from django.urls import path
from intranet import views


urlpatterns = [
    path('list/', views.IntranetListView.as_view(), name='intranet-list'),
]
