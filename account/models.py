from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import ValidationError


class UserRole(models.TextChoices):
    superuser = 'superuser', _("Super user")
    admin = 'admin', _("Admin")
    organization = 'organization', _("Organization")


class UserRoleManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.admin)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.superuser)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    role = models.CharField(max_length=32, choices=UserRole.choices)
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='admins',
                                     null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        if self.role == UserRole.organization and not self.organization_id:
            raise ValidationError({'type': _("Organization is required")})
