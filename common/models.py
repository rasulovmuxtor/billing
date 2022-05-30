from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    male = 'male', _("Male")
    female = "female", _("Female")


class BaseContact(models.Model):
    address = models.CharField(_("Address"), max_length=512, null=True, blank=True)
    phone = models.CharField(_("Phone number"), max_length=32, null=True, blank=True)
    email = models.EmailField(_("Email"), null=True, blank=True)

    class Meta:
        abstract = True
