# -*- coding: utf-8 -*-
"""
    test_checkout
    ~~~~~~~~~~~~~~~~~

    Tests for `checkout` module.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""
import requests
from flexmock import flexmock
from pytest import raises
from checkout import (
    Checkout,
    Contact,
    Payment,
    CheckoutException
)


class TestCheckoutException(object):
    def setup_method(self, method):
        self.exception = CheckoutException('message')

    def test_is_an_exception(self):
        assert isinstance(self.exception, Exception)

    def test_sets_error_message(self):
        assert self.exception.message == 'message'


class TestContactWithSomeParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            address='Esimerkkikatu 123',
            postcode='01234',
            postoffice='Helsinki',
            country='FIN'
        )

    def test_sets_first_name(self):
        assert self.contact.first_name == 'Matti'

    def test_sets_last_name(self):
        assert self.contact.last_name == 'Meikäläinen'

    def test_sets_address(self):
        assert self.contact.address == 'Esimerkkikatu 123'

    def test_sets_postal_code(self):
        assert self.contact.postcode == '01234'

    def test_sets_postal_office(self):
        assert self.contact.postoffice == 'Helsinki'

    def test_sets_country(self):
        assert self.contact.country == 'FIN'

    def test_phone_is_blank_by_default(self):
        assert self.contact.phone == ''

    def test_email_is_blank_by_default(self):
        assert self.contact.email == ''


class TestContactWithAllParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            email='matti.meikalainen@gmail.com',
            address='Esimerkkikatu 123',
            postcode='01234',
            postoffice='Helsinki',
            country='FIN',
            phone='020123456',
        )

    def test_sets_phone(self):
        assert self.contact.phone == '020123456'

    def test_sets_email(self):
        assert self.contact.email == 'matti.meikalainen@gmail.com'

    def test_dict(self):
        assert self.contact.dict == {
            'PHONE': '020123456',
            'EMAIL': 'matti.meikalainen@gmail.com',
            'FIRSTNAME': 'Matti',
            'FAMILYNAME': 'Meikäläinen',
            'ADDRESS': 'Esimerkkikatu 123',
            'POSTCODE': '01234',
            'POSTOFFICE': 'Helsinki',
            'COUNTRY': 'FIN'
        }


class TestPaymentWithMinimumParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            address='Esimerkkikatu 123',
            postcode='01234',
            postoffice='Helsinki',
            country='FIN'
        )
        self.payment = Payment(
            order_number='12345678',
            reference_number='9999999',
            amount='200',
            delivery_date='20140606',
            return_url='https://www.esimerkkikauppa.fi/sv/return',
            cancel_url='https://www.esimerkkikauppa.fi/sv/cancel',
            contact=self.contact
        )

    def test_sets_order_number(self):
        assert self.payment.order_number == '12345678'

    def test_sets_reference_number(self):
        assert self.payment.reference_number == '9999999'

    def test_sets_amount(self):
        assert self.payment.amount == '200'

    def test_sets_delivery_date(self):
        assert self.payment.delivery_date == '20140606'

    def test_sets_return_url(self):
        assert self.payment.return_url == \
            'https://www.esimerkkikauppa.fi/sv/return'

    def test_sets_cancel_url(self):
        assert self.payment.cancel_url == \
            'https://www.esimerkkikauppa.fi/sv/cancel'

    def test_sets_contact(self):
        assert self.payment.contact is self.contact

    def test_message_is_blank_by_default(self):
        assert self.payment.message == ''

    def test_currency_is_euro_by_default(self):
        assert self.payment.currency == 'EUR'

    def test_language_is_finnish_by_default(self):
        assert self.payment.language == 'FI'

    def test_delayed_url_is_blank_by_default(self):
        assert self.payment.delayed_url == ''

    def test_reject_url_is_blank_by_default(self):
        assert self.payment.reject_url == ''

    def test_unsupported_currency_raises_value_error(self):
        with raises(CheckoutException) as exc_info:
            self.payment.currency = 'USD'
        assert exc_info.value.message == \
            'Currently EUR is the only supported currency.'

    def test_language_can_be_finnish(self):
        self.payment.language = 'FI'
        assert self.payment.language == 'FI'

    def test_language_can_be_swedish(self):
        self.payment.language = 'SE'
        assert self.payment.language == 'SE'

    def test_language_can_be_english(self):
        self.payment.language = 'EN'
        assert self.payment.language == 'EN'

    def test_unsupported_locale_raises_value_error(self):
        with raises(CheckoutException) as exc_info:
            self.payment.language = 'DE'
        assert exc_info.value.message == \
            "Given language is not supported: 'DE'"

    def test_dict(self):
        assert self.payment.dict == {
            'VERSION': '0001',
            'STAMP': '12345678',
            'AMOUNT': '200',
            'REFERENCE': '9999999',
            'MESSAGE': '',
            'LANGUAGE': 'FI',
            'RETURN': 'https://www.esimerkkikauppa.fi/sv/return',
            'CANCEL': 'https://www.esimerkkikauppa.fi/sv/cancel',
            'REJECT': '',
            'DELAYED': '',
            'CURRENCY': 'EUR',
            'CONTENT': '1',
            'TYPE': '0',
            'ALGORITHM': '3',
            'DELIVERY_DATE': '20140606',
            'PHONE': '',
            'EMAIL': '',
            'FIRSTNAME': 'Matti',
            'FAMILYNAME': 'Meikäläinen',
            'ADDRESS': 'Esimerkkikatu 123',
            'POSTCODE': '01234',
            'POSTOFFICE': 'Helsinki',
            'COUNTRY': 'FIN'
        }

class TestPaymentWithAllParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            email='matti.meikalainen@gmail.com',
            address='Esimerkkikatu 123',
            postcode='01234',
            postoffice='Helsinki',
            country='FIN',
            phone='020123456',
        )
        self.payment = Payment(
            order_number='12345678',
            reference_number='9999999',
            amount='200',
            delivery_date='20140606',
            message='Esimerkkimaksun kuvaus',
            currency='EUR',
            language='FI',
            content='10',
            return_url='https://www.esimerkkikauppa.fi/sv/return',
            cancel_url='https://www.esimerkkikauppa.fi/sv/cancel',
            delayed_url='https://www.esimerkkikauppa.fi/sv/delayed',
            reject_url='https://www.esimerkkikauppa.fi/sv/reject',
            contact=self.contact
        )

    def test_sets_message(self):
        assert self.payment.message == 'Esimerkkimaksun kuvaus'

    def test_sets_currency(self):
        assert self.payment.currency == 'EUR'

    def test_sets_language(self):
        assert self.payment.language == 'FI'

    def test_sets_content(self):
        assert self.payment.content == '10'

    def test_sets_delayed_url(self):
        assert self.payment.delayed_url == \
            'https://www.esimerkkikauppa.fi/sv/delayed'

    def test_sets_reject_url(self):
        assert self.payment.reject_url == \
            'https://www.esimerkkikauppa.fi/sv/reject'

    def test_dict(self):
        assert self.payment.dict == {
            'VERSION': '0001',
            'STAMP': '12345678',
            'AMOUNT': '200',
            'REFERENCE': '9999999',
            'MESSAGE': 'Esimerkkimaksun kuvaus',
            'LANGUAGE': 'FI',
            'RETURN': 'https://www.esimerkkikauppa.fi/sv/return',
            'CANCEL': 'https://www.esimerkkikauppa.fi/sv/cancel',
            'REJECT': 'https://www.esimerkkikauppa.fi/sv/reject',
            'DELAYED': 'https://www.esimerkkikauppa.fi/sv/delayed',
            'CURRENCY': 'EUR',
            'CONTENT': '10',
            'TYPE': '0',
            'ALGORITHM': '3',
            'DELIVERY_DATE': '20140606',
            'PHONE': '020123456',
            'EMAIL': 'matti.meikalainen@gmail.com',
            'FIRSTNAME': 'Matti',
            'FAMILYNAME': 'Meikäläinen',
            'ADDRESS': 'Esimerkkikatu 123',
            'POSTCODE': '01234',
            'POSTOFFICE': 'Helsinki',
            'COUNTRY': 'FIN'
        }

class TestPaymentWithoutContact(object):
    def setup_method(self, method):
        self.payment = Payment(
            order_number='12345678',
            reference_number='9999999',
            amount='200',
            delivery_date='20140606',
            message='Esimerkkimaksun kuvaus',
            currency='EUR',
            language='FI',
            content='10',
            return_url='https://www.esimerkkikauppa.fi/sv/return',
            cancel_url='https://www.esimerkkikauppa.fi/sv/cancel',
            delayed_url='https://www.esimerkkikauppa.fi/sv/delayed',
            reject_url='https://www.esimerkkikauppa.fi/sv/reject',
        )

    def test_dict(self):
        assert self.payment.dict == {
            'VERSION': '0001',
            'STAMP': '12345678',
            'AMOUNT': '200',
            'REFERENCE': '9999999',
            'MESSAGE': 'Esimerkkimaksun kuvaus',
            'LANGUAGE': 'FI',
            'RETURN': 'https://www.esimerkkikauppa.fi/sv/return',
            'CANCEL': 'https://www.esimerkkikauppa.fi/sv/cancel',
            'REJECT': 'https://www.esimerkkikauppa.fi/sv/reject',
            'DELAYED': 'https://www.esimerkkikauppa.fi/sv/delayed',
            'CURRENCY': 'EUR',
            'CONTENT': '10',
            'TYPE': '0',
            'ALGORITHM': '3',
            'DELIVERY_DATE': '20140606',
            'PHONE': '',
            'EMAIL': '',
            'FIRSTNAME': '',
            'FAMILYNAME': '',
            'ADDRESS': '',
            'POSTCODE': '',
            'POSTOFFICE': '',
            'COUNTRY': ''
        }

class TestCheckout(object):
    def test_defaults_to_merchant_test_account(self):
        checkout = Checkout()
        assert checkout.merchant_id == '375917'
        assert checkout.merchant_secret == 'SAIPPUAKAUPPIAS'

    def test_custom_merchant_credentials(self):
        checkout = Checkout(merchant_id='12345', merchant_secret='secret')
        assert checkout.merchant_id == '12345'
        assert checkout.merchant_secret == 'secret'

class TestReturnChecksum(object):
    def test_validate_payment_valid_return(self):
        checkout = Checkout()
        assert checkout.validate_payment_return(
            mac="2657BA96CC7879C79192547EB6C9D4082EA39CA52FE1DAD09CB1C632ECFDAE67",
            version="0001",
            order_number="1388998411",
            order_reference="474738238",
            payment="12288575",
            status="3",
            algorithm="3"
        )

    def test_validate_payment_invalid_return(self):
        checkout = Checkout()
        assert not checkout.validate_payment_return(
            mac="2657BA96CC7879C79192547EB6C9D4082EA39CA52FE1DAD09CB1C632ECFDAE68",
            version="0001",
            order_number="1388998411",
            order_reference="474738238",
            payment="1221238575",
            status="3",
            algorithm="3"
        )

class TestParameterLimitation(object):
    def test_exception_generation(self):
        with raises(CheckoutException) as exc_info:
            payment = Payment(
                order_number='12345678',
                reference_number='99999999999999999999999999999999999999999999',
                amount='200',
                delivery_date='20140606',
                message='Esimerkkimaksun kuvaus',
                currency='EUR',
                language='FI',
                content='10',
                return_url='https://www.esimerkkikauppa.fi/sv/return',
                cancel_url='https://www.esimerkkikauppa.fi/sv/cancel',
                delayed_url='https://www.esimerkkikauppa.fi/sv/delayed',
                reject_url='https://www.esimerkkikauppa.fi/sv/reject',
            )

        assert exc_info.value.message == \
            'reference_number over maximum allowed 20 characters'

    def test_parameter_clipping(self):
        contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            address='Esimerkkikatu 123',
            postcode='01234123123123123123123123123123123123123',
            postoffice='Helsinki',
            country='FIN'
        )
        assert len(contact.postcode) == 14
