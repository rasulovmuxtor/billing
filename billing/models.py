from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='reports',
                                     verbose_name=_("Organization"))
    total_students = models.BigIntegerField(_("Total students"),default=0)
    total_groups = models.BigIntegerField(_("Total groups"),default=0)
    total_income = models.DecimalField(_("Total income"), max_digits=25, decimal_places=2,default=0)
    overpayment = models.DecimalField(_("Overpayment"), max_digits=25, decimal_places=2,default=0)
    debt = models.DecimalField(_("Debt"), max_digits=25, decimal_places=2,default=0)

    reported_at = models.DateTimeField(_("Reported at"), auto_now_add=True)
    excel = models.FileField(_("Excel"),upload_to="reports")

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class StudentReport(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE,
                                     related_name='student_reports',
                                     verbose_name=_("Organization"))
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='reports',
                                verbose_name=_("Student"))
    delta = models.DecimalField(_("Delta"), max_digits=18, decimal_places=2)
    expected = models.DecimalField(_("Expected amount"), max_digits=18, decimal_places=2)

    reported_at = models.DateTimeField(_("Reported at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Student Report")
        verbose_name_plural = _("Student Reports")
