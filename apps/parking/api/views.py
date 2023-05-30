from rest_framework.viewsets import ModelViewSet
from ..models import Booking, Customer
from .serializers import BookingSerializer, BookingListSerializer, CustomerSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from rest_framework.views import APIView
from ..models import parking_bay_choices
from django_filters.rest_framework import DjangoFilterBackend

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class CustomerView(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination    

class BookingView(ModelViewSet):
    queryset = Booking.objects.select_related('customer').all()
    serializer_class = BookingSerializer
    pagination_class = StandardPagination   
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parking_bay', 'booking_date', 'customer']

    def validate_booking(self, data):
        """
        Method to check whether the booking should be made or not according to various requirements.
        rtype: bool, str
        """

        # Check if the customer has already made the booking for the given date.
        if Booking.objects.filter(customer = data['customer'], booking_date = data['booking_date']).exists():
            return False, 'Customer can only make one booking a day.'

        # Check if the booking is made at least 24 hrs in advance or not.
        # First check whether the booking is scheduled in the past or not.
        booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d')
        diff = (booking_date - datetime.now()).total_seconds()

        if booking_date < datetime.now():
            return False, 'Booking date cannot be in the past.'
        else:
            if diff < 86400:
                return False, 'Booking must be made at least 24 hrs in advance.'

        # Check if parking bay is available for the given date.        
        if Booking.objects.filter(parking_bay = data['parking_bay'], booking_date = data['booking_date']).exists():
            return False, 'Parking Bay {} has already been booked. Please select another bay to complete the booking.'.format(data['parking_bay'])

        return True, ''

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return BookingSerializer
        elif self.request.method == 'GET':
            return BookingListSerializer
        return BookingSerializer

    def create(self, request, *args, **kwargs):
        valid, msg = self.validate_booking(request.data)
        if valid:
            return super().create(request, *args, **kwargs)
        else:
            return Response(msg, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        valid, msg = self.validate_booking(request.data)
        if valid:
            return super().update(request, *args, **kwargs)
        else:
            return Response(msg, status = status.HTTP_400_BAD_REQUEST)

class ParkingView(APIView):
    def get(self, request, date, *args, **kwargs):
        reserved = []
        free = []
        for key, _ in parking_bay_choices:
            if Booking.objects.filter(parking_bay = key, booking_date = date).exists():
                reserved.append(key)
            else:
                free.append(key)
        return Response({
                'free': free,
                'reserved': reserved
            },
            status = status.HTTP_200_OK  
        )