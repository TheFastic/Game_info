from django.urls import path
from . import views
from .views import ProfileView, FriendListView, SettingUpdateView, FriendRequestView

urlpatterns = [
    path("registretion/", views.register_view,name="registretion"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profil/", ProfileView.as_view(), name="profil"),
    path("friends/", FriendListView.as_view(), name="friends"),
    path("setting/", SettingUpdateView.as_view(), name="settings"),
    path("request/<int:id>", FriendRequestView.as_view(), name="friends_request")
]