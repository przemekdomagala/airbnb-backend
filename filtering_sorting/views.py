from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer
from .filters.criteria import (PriceCriteria, LocationCriteria, RatingCriteria,
                                AmenityCriteria, DistanceCriteria, PropertyTypeCriteria,
                                ReviewCountCriteria)
from .filters.concrete_filters import (PriceFilter, LocationFilter, RatingFilter,
                                       AmenityFilter, DistanceFilter, PropertyTypeFilter,
                                       ReviewCountFilter)

class FilteredPropertyListAPIView(APIView):
    def get(self, request):
        queryset = Property.objects.all()

        # --- Zbieramy parametry GET ---
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        location = request.GET.get('location')
        min_rating = request.GET.get('min_rating')
        max_rating = request.GET.get('max_rating')
        amenities = request.GET.getlist('amenities')  # amenities może być listą!
        max_distance = request.GET.get('max_distance')
        property_types = request.GET.getlist('property_types')  # typy nieruchomości
        min_reviews = request.GET.get('min_reviews')

        # --- Tworzymy filtry na podstawie parametrów ---
        filters = []

        if price_min and price_max:
            price_criteria = PriceCriteria()
            price_criteria.set_criteria(float(price_min), float(price_max))
            filters.append(PriceFilter(price_criteria))

        if location:
            location_criteria = LocationCriteria()
            location_criteria.set_criteria(location)
            filters.append(LocationFilter(location_criteria))

        if min_rating and max_rating:
            rating_criteria = RatingCriteria()
            rating_criteria.set_criteria(float(min_rating), float(max_rating))
            filters.append(RatingFilter(rating_criteria))

        if amenities:
            amenity_criteria = AmenityCriteria()
            amenity_criteria.set_criteria(amenities)
            filters.append(AmenityFilter(amenity_criteria))

        if max_distance:
            distance_criteria = DistanceCriteria()
            distance_criteria.set_criteria(float(max_distance))
            filters.append(DistanceFilter(distance_criteria))

        if property_types:
            property_type_criteria = PropertyTypeCriteria()
            property_type_criteria.set_criteria(property_types)
            filters.append(PropertyTypeFilter(property_type_criteria))

        if min_reviews:
            review_count_criteria = ReviewCountCriteria()
            review_count_criteria.set_criteria(int(min_reviews))
            filters.append(ReviewCountFilter(review_count_criteria))

        # --- Aplikujemy filtry ---
        for f in filters:
            queryset = f.apply(queryset)

            # Sprawdzamy, czy filtr zwrócił listę — tylko wtedy kontynuujemy na liście
            if isinstance(queryset, list):
                # Jak już dostaliśmy listę, to wszystkie następne filtry muszą też działać na liście!
                pass


        # --- Serializujemy i zwracamy odpowiedź ---
        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)
