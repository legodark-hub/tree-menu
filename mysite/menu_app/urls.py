from django.urls import path
from . import views

urlpatterns = [
    path('menu-example/', views.menu_example, name='menu_example'),
]