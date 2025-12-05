from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Users, UserProfile, Friends, Setting
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.contrib.auth import login as auth_login
from .forms import RegisterForm
from django.db.models import Q

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        UserProfile.objects.create(user=user)
        Setting.objects.create(user=user)

        login(request, user)
        return redirect("home")

    return render(request, "login_adn_registret/register.html", {"form": form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("home")

    return render(request, "login_adn_registret/login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, DetailView):
    model = Users
    template_name = 'user/detail.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'user_id'

    def get_queryset(self):
        return Users.objects.select_related("settings", "profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viewer = self.request.user
        owner = self.get_object()
        context['can_view'] = self.user_can_view(viewer, owner)
        return context

    def user_can_view(self, viewer, owner):
        if owner.settings.profile_public or viewer == owner:
            return True

        return Friends.objects.filter(
            Q(sender=viewer, receiver=owner) |
            Q(sender=owner, receiver=viewer), 
            status='accepted').exists()
    
class FriendListView(LoginRequiredMixin, ListView):
    model = Friends
    template_name = 'friends/list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        user = self.request.user
        return Friends.objects.filter(
            Q(sender=user) | Q(receiver=user),
            status='accepted'
        ).select_related("sender", "receiver")
    
class SettingUpdateView(LoginRequiredMixin, UpdateView):
    model = Setting
    template_name = 'settings/update.html'
    fields = ['nickname', 'profile_background', 'profile_public']
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return Setting.objects.get(user=self.request.user)
    
class FriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver = get_object_or_404(Users, id=kwargs.get('user_id'))

        if sender == receiver:
            return HttpResponseForbidden("Неможливо додати себе")

        Friends.objects.get_or_create(
            sender=sender,
            receiver=receiver,
            defaults={"status": "pending"}
        )

        return redirect('friend_list')