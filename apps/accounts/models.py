# APP: accounts
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superusers must have a password")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the username.
    Username is removed.
    """
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    email = models.EmailField(unique=True)

    # Required Django admin fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_picture = models.CloudinaryField("image", blank=True, null=True)

    # Google login fields (optional)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)  # Google profile picture

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No username

    def __str__(self):
        return self.email

class ShippingAddress(models.Model):
    ADDRESS_LABELS = [
        ("home", "Home"),
        ("office", "Office"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipping_addresses"
    )
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    zone = models.ForeignKey(
        "ShippingZone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipping_addresses"
    )
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Nepal")
    is_default = models.BooleanField(default=False)
    label = models.CharField(max_length=20, choices=ADDRESS_LABELS, default="home")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.address_line1}"

class ShippingZone(models.Model):
    SHIPPING_ZONES = [
        ("inside_valley", "Inside Kathmandu Valley"),
        ("outside_valley", "Outside Kathmandu Valley"),
    ]
    name = models.CharField(max_length=20, choices=SHIPPING_ZONES)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name