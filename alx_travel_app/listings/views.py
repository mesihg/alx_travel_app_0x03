from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing listings.
    Provides CRUD operations for Listing model.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    def perform_create(self, serializer):
        """Set the host to the current user when creating a listing."""
        serializer.save(host=self.request.user)
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific listing."""
        listing = self.get_object()
        bookings = listing.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific listing."""
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    Provides CRUD operations for Booking model.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def perform_create(self, serializer):
        """Set the user to the current user and calculate total price when creating a booking."""
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        # Calculate the number of nights
        nights = (end_date - start_date).days
        total_price = nights * listing.price_per_night
        
        serializer.save(user=self.request.user, total_price=total_price)
    
    def get_queryset(self):
        """Filter bookings to show only the current user's bookings."""
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.none()

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    Provides CRUD operations for Review model.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        """Set the user to the current user when creating a review."""
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """Filter reviews to show only the current user's reviews."""
        if self.request.user.is_authenticated:
            return Review.objects.filter(user=self.request.user)
        return Review.objects.none()
