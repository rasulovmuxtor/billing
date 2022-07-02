from django.contrib import admin
from billing import models


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reported_at', 'organization']

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(organization_id=organization_id)
        return queryset


@admin.register(models.StudentReport)
class StudentReportAdmin(admin.ModelAdmin):
    list_display = ['reported_at', 'student']

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        organization_id = request.user.organization_id
        if organization_id:
            return queryset.filter(organization_id=organization_id)
        return queryset
