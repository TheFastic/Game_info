from django.contrib import admin
from .models import Titel, Comment, Genres

admin.site.register(Titel)
admin.site.register(Comment)
admin.site.register(Genres)