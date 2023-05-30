from rest_framework import routers
from .views import BookingView, CustomerView, ParkingView
from django.urls import path

router = routers.DefaultRouter()
router.register('booking', BookingView)
router.register('customer', CustomerView)

urlpatterns = [
    path('parking/<str:date>/', ParkingView.as_view(), name = 'api-v1-parking-view')
]

urlpatterns += router.urls