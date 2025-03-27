from django.urls import path
from uxg import views

app_name = 'uxg'

urlpatterns = [
    path("", views.index, name="index"),
    path("communities/", views.community_page, name="communities"),
    path("createnewpost/", views.create_post, name="create_new_post"),
    path("signup/", views.register, name="signup"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile, name="profile"),
    path('logout/', views.logout_view, name='logout'),
    path('edit_bio/', views.edit_bio, name='edit_bio'),

]