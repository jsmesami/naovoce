from decimal import Decimal
from django.db import models
from django.conf import settings


class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)


class PayPalResponse(models.Model):
    donation = models.ForeignKey(Donation, null=True)

    payment_id = models.CharField(max_length=256, null=True, blank=True, db_index=True)
    currencycode = models.CharField(max_length=32, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)

    status = models.CharField(max_length=256, null=True, blank=True)
    raw_response = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def fill_from_response(self, payment, donationNumber):
        transaction = payment.transactions[0]
        amount = Decimal(transaction.amount.total)

        self.donation_id = donationNumber
        self.payment_id = payment.id
        self.amount = amount
        self.currencycode = transaction.amount.currency
        self.status = payment.state
        self.raw_response = str(payment)


    class Meta:
        verbose_name = "PayPal Response"
        verbose_name_plural = "PayPal Responses"
