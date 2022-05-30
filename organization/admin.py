from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from organization import models
from common.utils import number_style


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'phone', 'balance_')
    search_fields = ('title', 'phone')
    autocomplete_fields = ('parent',)

    def balance_(self, obj):
        return mark_safe(number_style(obj.balance))

    balance_.short_description = _("Balance")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(id=organization_id)
        return queryset


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone')
    search_fields = ('full_name', 'phone')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(organization_id=organization_id)
        return queryset


@admin.register(models.Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price')
    search_fields = ('title',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(organization_id=organization_id)
        return queryset


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', 'tariff')
    search_fields = ('title',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(organization_id=organization_id)
        return queryset
