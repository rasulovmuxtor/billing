from django.contrib import admin
from student import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from common.utils import number_style


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'balance_')
    search_fields = ('full_name',)

    def balance_(self, obj):
        return mark_safe(number_style(obj.balance))

    balance_.short_description = _("Balance")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(group__organization_id=organization_id)
        return queryset


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount_', 'type', 'identifier', 'created_at')
    search_fields = ('id', 'identifier')
    autocomplete_fields = ['student']
    readonly_fields = ['created_at']
    list_filter = ['type']

    def amount_(self, obj):
        return mark_safe(number_style(obj.amount))

    amount_.short_description = _("Amount")

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(student__group__organization_id=organization_id)
        return queryset
