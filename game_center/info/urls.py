from django.urls import path
from .views import TitelListView, TitelDetailView, TitelCreateView, TitelUpdateView, TitelDeleteView, add_comment

urlpatterns = [
    path("", TitelListView.as_view(), name="titel_list"),
    path("<int:pk>/", TitelDetailView.as_view(), name="titel_detail"),
    path("create/", TitelCreateView.as_view(), name="titel_create"),
    path("<int:pk>/edit/", TitelUpdateView.as_view(), name="titel_update"),
    path("<int:pk>/delete/", TitelDeleteView.as_view(), name="titel_delete"),
    path("<int:titel_id>/comment/", add_comment, name="add_comment"),
]