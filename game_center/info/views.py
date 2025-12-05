from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Titel, Comment

class TitelListView(ListView):
    model = Titel
    template_name = "titel/titel_list.html"
    context_object_name = "titels"
    ordering = "-created_at"

class TitelDetailView(DetailView):
    model = Titel
    template_name = "titel/detail.html"
    context_object_name = "titel"

class TitelCreateView(LoginRequiredMixin, CreateView):
    model = Titel
    template_name = "titel/create.html"
    fields = ["titel", "description", "img_icon", "img_background"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TitelUpdateView(LoginRequiredMixin, UpdateView):
    model = Titel
    template_name = "titel/update.html"
    fields = ["titel", "description", "img_icon", "img_background"]

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return HttpResponseForbidden("Ви не автор!")
        return super().dispatch(request, *args, **kwargs)

class TitelDeleteView(LoginRequiredMixin, DeleteView):
    model = Titel
    template_name = "titel/delete.html"
    success_url = reverse_lazy("titel_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return HttpResponseForbidden("Ви не автор!")
        return super().dispatch(request, *args, **kwargs)
    
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, titel_id):
    titel = get_object_or_404(Titel, id=titel_id)

    if request.method == "POST":
        text = request.POST.get("text")
        Comment.objects.create(
            titel=titel,
            author=request.user,
            text=text
        )
    return redirect("titel_detail", pk=titel.id)

