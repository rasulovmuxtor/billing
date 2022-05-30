from django.db import models
from common.models import BaseContact
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver



class Student(BaseContact):
    """
    If tariff is null, use its price to charge
    If tariff is not null, use group's price to charge
    """

    full_name = models.CharField(_("Full name"), max_length=255)
    group = models.ForeignKey('organization.Group', on_delete=models.CASCADE, related_name='students')
    tariff = models.ForeignKey('organization.Tariff', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='students')
    date_of_birth = models.DateField(_("Date of birth"))
    balance = models.DecimalField(_("Balance"), max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ('full_name',)

    def get_tariff(self):
        if self.tariff:
            return self.tariff
        return self.group.tariff

    def __str__(self):
        return self.full_name

    def get_fee(self):
        expected = self.get_tariff().price - self.balance
        if expected > 0:
            return expected
        return 0


class TransactionType(models.IntegerChoices):
    cash = 1, _("Cash")
    bank = 2, _("Bank")
    stripe=3,_("Stripe")
    charge = -1, _("Charge")


class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transactions',
                                verbose_name=_("Student"))
    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=2)
    type = models.SmallIntegerField(_("Type"), choices=TransactionType.choices)
    identifier = models.CharField(_("External identifier"), max_length=512, null=True, blank=True,
                                  help_text=_("Payment service or bank transaction id"))
    comment = models.TextField(_("Comment"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def clean(self):
        if self.amount == 0:
            raise ValidationError({'amount': _("can't be 0")})
        elif self.type < 0 and self.amount > 0:
            raise ValidationError({'amount': _("must be less than 0")})
        elif self.type > 0 and self.amount < 0:
            raise ValidationError({'amount': _("must be greater than 0")})

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return str(self.id)



@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance: Transaction, created, *args, **kwargs):
    if created:
        student = instance.student
        student.balance += instance.amount
        student.save(update_fields=['balance'])