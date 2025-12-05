from django.db import models
from core.models import Users

class Titel(models.Model):

    titel = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    img_icon = models.ImageField(upload_to="avatars/", blank=True, null=True)
    img_background = models.ImageField(upload_to="background/", blank=True, null=True)
    genres = models.ManyToManyField("Genres", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="titel",verbose_name="Автор", null=True)

    def __str__(self):
        return f"{self.titel}"

class Comment(models.Model):

    titel = models.ForeignKey(Titel, on_delete=models.CASCADE, related_name="comments",verbose_name="Статья", null=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="comments",verbose_name="Автор", null=True)
    text = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")


    def __str__(self):
        return f"Коментар від {self.author.username}"    


class Genres(models.Model):
    TITEL_GENRE = [
        ("horors", "Horors"),
        ("shooter", "Shooter"),
        ("survival", "Survival"),
        ("tower defense", "Tower of Defense"),
        ("battleground", "Battleground"),
        ("mmorpg", "MMORPG"),
        ("multiplayer", "Multiplayer"),
        ("roleplay", "Roleplay"),
    ]

    genre = models.CharField(max_length=50, choices=TITEL_GENRE, null=True)

    def __str__(self):
        return f"{self.genre}"
    