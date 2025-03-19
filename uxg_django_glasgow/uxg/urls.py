from django.urls import path
from uxg import views

app_name = 'uxg'

urlpatterns = [
    path("", views.index, name="index"),
    path("communities/", views.community_page, name="communities"),
    path("createnewpost/", views.create_post, name="create_new_post"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
]