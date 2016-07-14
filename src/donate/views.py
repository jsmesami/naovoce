import logging
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from .paypal import PayPal
from .models import Donation
from . import forms


class DonateView(View):

    template_name = 'donate/donate.html'

    def get(self, request):
        return render(request, self.template_name, {'form': forms.DonateForm()})

    def post(self, request):
        form = forms.DonateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            donation = Donation.objects.create(amount=data['amount'])
            return redirect('donate:init-paypal', donation_id=donation.id)
        else:
            return render(request, self.template_name, {'form': form})


class PayPalView(View):

    def get_driver(self) -> PayPal:
        return PayPal(**settings.PAYPAL)

    def get(self, request, action: str, donation_id: str):
        if action == 'init':
            donation = Donation.objects.get(id=donation_id)
            return self.handle_init(request, donation)
        elif action == 'return':
            return self.handle_confirm(request)
        elif action == 'cancel':
            return self.handle_cancel(request)

    def handle_init(self, request, donation: Donation):
        '''
        Initiate the checkout and render payment form.
        '''
        driver = self.get_driver()
        result = driver.create_payment(
            amount = str(donation.amount),
            donation_number = donation.id,
            donation_description = _('Na-ovoce donation number {donation.id}').format(donation=donation),
            return_url = request.build_absolute_uri(reverse('donate:paypal', kwargs={'action': 'return'})),
            cancel_url = request.build_absolute_uri(reverse('donate:paypal', kwargs={'action': 'cancel'})),
        )
        if result:
            return redirect(driver.gateway_url())
        else:
            logging.error('Donation ID = %d: PayPal driver API error = %r.', donation.id, driver.payment.error)
            messages.error(request, _('We were unable to start a PayPal transaction. Please try again.'))
            return redirect('donate:index')

    def handle_confirm(self, request):
        '''
        The user has returned from PayPal. We need to execute the payment.
        '''
        driver = self.getDriver()
        payment_id = request.GET['paymentId']
        payer_id = request.GET['PayerID']

        result = driver.execute_payment(payment_id, payer_id)

        if result:
            return redirect('donate:thank-you')
        else:
            logging.error('Payment ID = %r: PayPal charge failed; error = %r.', payment_id, driver.payment.error)
            messages.error(request, _('We were unable to complete the transaction. Your card has not been charged. Please try again.'))
            return redirect('donate:index')

    def handle_cancel(self, request):
        '''
        The user has returned from PayPal, but he canceled the payment.
        '''

        messages.error(request, _('We were unable to complete the transaction. Your card has not been charged. Please try again.'))
        return redirect('donate:index')


class ThankYouView(View):

    def get(self, request):
        return render(request, 'donate/thank-you.html')
