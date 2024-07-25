from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projekt/<int:pk>/', views.projekt, name='projekt'),
    path('neues_projekt/', views.new_projekt, name='neues_projekt'),
    path('kategorie/<int:pr_pk>/<int:kat_pk>/', views.kategorie, name='kategorie'),
    path('auswertung/<int:pk>/', views.auswertung, name='auswertung'),
    path('kategorie_auswertung/<int:pr_pk>/<int:kat_pk>/', views.kategorie_auswertung, name='kategorie_auswertung'),
    path('gesamt_auswertung/<int:pk>/', views.gesamt_auswertung, name='gesamt_auswertung'),

]