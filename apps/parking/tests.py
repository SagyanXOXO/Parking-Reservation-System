from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Booking
from apps.parking.api.serializers import CustomerSerializer, BookingSerializer, BookingListSerializer

class CustomerTests(APITestCase):
    def test_create_customer(self):
        """
        Ensure we can create customer object.
        """
        url = reverse('customer-list')
        data = {
            "name": "Jane Doe",
            "license_plate": "ABSx123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_customer(self):
        """
        Ensure we can get customer objects.
        """
        url = reverse('customer-list')
        customer = Customer.objects.all()
        data = CustomerSerializer(customer, many = True).data
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], data)

class BookingTests(APITestCase):
    def test_create_get_booking(self):
        """
        Ensure we can create booking object.
        """
        url = reverse('booking-list')
        customer = Customer.objects.create(
            name = 'Jane Doe',
            license_plate = 'ABSx123'
        )
        payload = {
            "customer": customer.id,
            "parking_bay": 1,
            "booking_date": '2023-06-01'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = Booking.objects.all()
        data = BookingListSerializer(booking, many = True).data
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.data['results'], data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_multiple_booking(self):
        url = reverse('booking-list')
        customer = Customer.objects.create(
            name = 'Jane Doe',
            license_plate = 'ABSx123'
        )
        payload = {
            "customer": customer.id,
            "parking_bay": 1,
            "booking_date": '2023-06-01'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        customer = Customer.objects.create(
            name = 'John Doe',
            license_plate = 'Axl35f'
        )
        payload = {
            "customer": customer.id,
            "parking_bay": 1,
            "booking_date": '2023-06-01'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "customer": customer.id,
            "parking_bay": 2,
            "booking_date": '2023-06-01'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


