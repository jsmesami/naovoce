import paypalrestsdk

from .models import PayPalResponse

class PayPal(object):

    def __init__(self, client_id: str, client_secret: str, development: bool):
        paypalrestsdk.configure({
          'mode':  'sandbox' if development else 'live',
          'client_id': client_id,
          'client_secret': client_secret
        })

    def save_response_data(self, r, donationNumber = None):
        response = PayPalResponse()
        response.fill_from_response(r, donationNumber)
        response.save()

    def create_payment(self, amount: str, donation_number: int, donation_description: str, return_url: str, cancel_url: str):
        payment = paypalrestsdk.Payment({
        'intent': 'sale',
                'redirect_urls': {
                    'return_url': return_url,
                    'cancel_url': cancel_url
                },
                'payer': {
                    'payment_method': 'paypal'
                },
                'transactions': [{
                    'item_list': {
                        'items': [{
                            'name': donation_description,
                            'price': amount,
                            'currency': 'CZK',
                            'quantity': 1}]},
                    'amount': {
                        'total': amount,
                        'currency': 'CZK'
                    },
                    'description': donation_description
                }]
        })

        result = payment.create()
        self.save_response_data(payment, donation_number)
        self.payment = payment
        return result

    def gateway_url(self):
        return list(filter(lambda link: link['rel'] == 'approval_url', self.payment.links))[0]['href']

    def execute_payment(self, payment_id, payer_id):
        '''
        http://localhost:8000/process?paymentId=PAY-4MU4554885109922RK5WY6RY&token=EC-7KA58850T52481227&PayerID=5N9AC7EPXJP9C
        '''
        payment = paypalrestsdk.Payment.find(payment_id)

        result = payment.execute({'payer_id': payer_id})
        self.save_response_data(payment)
        self.payment = payment
        return result
