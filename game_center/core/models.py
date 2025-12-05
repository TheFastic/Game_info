from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Поле username є обов'язковим")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, **extra_fields)
    

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Профіль {self.user.username}"
    

class Groups(models.Model):
    name = models.CharField(max_length=30, unique=True)
    members = models.ManyToManyField(Users, related_name="custom_groups")

    def __str__(self):
        return self.name
    

class GroupsInfo(models.Model):
    group = models.OneToOneField(Groups, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="group_logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Кабінет групи {self.group.name}"
    
    
class Friends(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("blocked", "Blocked"),
    ]

    sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="friend_requests_sent")
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="friend_requests_received")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        return f"{self.sender} {self.receiver} ({self.status})"
    

class Setting(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="settings")

    profile_background = models.ImageField(
        upload_to="profile_backgrounds/",
        blank=True,
        null=True
    )
    profile_public = models.BooleanField(default=False)

    nickname = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Налаштування {self.user.username}"
