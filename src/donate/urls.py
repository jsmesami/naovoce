from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.DonateView.as_view(), name='index'),
    url(r'^paypal/init/(?P<donation_id>\d+)$', views.PayPalView.as_view(), { 'action': 'init' }, name='init-paypal'),
    url(r'^paypal/(?P<action>init|return|cancel)$', views.PayPalView.as_view(), { 'donation_id': None }, name='paypal'),
    url(r'^thank-you$', views.ThankYouView.as_view(), name='thank-you'),
]
