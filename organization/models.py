from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseContact


class Organization(BaseContact):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='branches', null=True, blank=True)
    title = models.CharField(_("Title"), max_length=255)
    balance = models.DecimalField(_("Balance"), max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ('id', 'parent_id')

    def __str__(self):
        return self.title


class Teacher(BaseContact):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teachers',
                                     verbose_name=_("Organization"))
    full_name = models.CharField(_("Full name"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        ordering = ('organization_id', 'id')

    def __str__(self):
        return self.full_name


class Tariff(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tariffs',
                                     verbose_name=_("Organization"))
    title = models.CharField(_("Title"), max_length=255)
    price = models.DecimalField(_("Price"), max_digits=18, decimal_places=2)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Tariff")
        verbose_name_plural = _("Tariffs")
        ordering = ('organization_id', 'id')

    def __str__(self):
        return self.title


class Group(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='groups',
                                     verbose_name=_("Organization"))
    title = models.CharField(_("Title"), max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='groups', verbose_name=_("Teacher"))
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, related_name='groups', verbose_name=_("Tariff"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ('organization_id', 'id')

    def __str__(self):
        return self.title
