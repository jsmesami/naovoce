from django.test import TestCase
from django.core.urlresolvers import reverse
from unittest.mock import patch, Mock

from .models import Donation

DONATED_AMOUNT = 1000

class DonateViewTest(TestCase):


    def test_display_donation_form(self):
        response = self.client.get(reverse('donate:index'))
        self.assertTemplateUsed(response, 'donate/donate.html')

    def test_save_donation_form(self):
        response = self.client.post(reverse('donate:index'), {'amount': DONATED_AMOUNT})
        donation = Donation.objects.get(amount=DONATED_AMOUNT)
        self.assertRedirects(response, reverse('donate:init-paypal', kwargs = { 'donation_id': donation.id}), fetch_redirect_response = False)

    @patch('donate.views.PayPal', new=Mock(return_value=Mock(gateway_url=Mock(return_value='http://example.com/'),
                                                             create_payment=Mock(return_value=True))))
    def test_init_payment(self):
        donation = Donation.objects.create(amount=DONATED_AMOUNT)
        response = self.client.get(reverse('donate:init-paypal', kwargs = { 'donation_id': donation.id}))
        self.assertRedirects(response, 'http://example.com/')


    @patch('donate.views.PayPal', new=Mock(return_value=Mock(execute_payment=Mock(return_value=True))))
    def test_execute_payment(self):
        response = self.client.get(reverse('donate:paypal', kwargs = { 'action': 'return'}) + '?paymentId=payment1&PayerID=payer1')
        self.assertRedirects(response, reverse('donate:thank-you'))

    def test_cancel_tells_user_that_he_canceled(self):
        response = self.client.get(reverse('donate:paypal', kwargs = { 'action': 'cancel'}))
        self.assertRedirects(response, reverse('donate:index'))
