from django.urls import path
from . import views

urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
    path('del_comment', views.del_comment, name='del_comment'),
]