from django.urls import path
from uxg import views

app_name = 'uxg'

urlpatterns = [
    path("", views.index, name="index"), 
    path("createnewpost/", views.create_post, name="create_new_post"),
]
