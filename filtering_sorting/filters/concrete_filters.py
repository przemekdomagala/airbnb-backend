from .abstract_filter import AbstractFilter
from .criteria import (PriceCriteria, LocationCriteria, RatingCriteria,
                       AmenityCriteria, DistanceCriteria, PropertyTypeCriteria,
                       ReviewCountCriteria)
from django.db import connection

class PriceFilter(AbstractFilter):
    def __init__(self, criteria: PriceCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if self.criteria.min_price is not None and self.criteria.max_price is not None:
            if isinstance(queryset, list):
                # Filtrowanie na liście
                return [
                    prop for prop in queryset
                    if self.criteria.min_price <= prop.price_per_night <= self.criteria.max_price
                ]
            else:
                # Filtrowanie na QuerySecie
                return queryset.filter(
                    price_per_night__gte=self.criteria.min_price,
                    price_per_night__lte=self.criteria.max_price
                )
        return queryset


class LocationFilter(AbstractFilter):
    def __init__(self, criteria: LocationCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if self.criteria.location_id:
            if isinstance(queryset, list):
                # Filtrowanie ręczne listy
                return [
                    prop for prop in queryset
                    if self.criteria.location_id.lower() in prop.location.lower()
                ]
            else:
                # Filtrowanie na QuerySecie
                return queryset.filter(location__icontains=self.criteria.location_id)
        return queryset


class RatingFilter(AbstractFilter):
    def __init__(self, criteria: RatingCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if self.criteria.min_rating is not None and self.criteria.max_rating is not None:
            if isinstance(queryset, list):
                return [
                    prop for prop in queryset
                    if self.criteria.min_rating <= prop.rating <= self.criteria.max_rating
                ]
            else:
                return queryset.filter(
                    rating__gte=self.criteria.min_rating,
                    rating__lte=self.criteria.max_rating
                )
        return queryset

class AmenityFilter(AbstractFilter):
    def __init__(self, criteria: AmenityCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if not self.criteria.amenities:
            return queryset

        # WYKRYWAMY czy używamy PostgreSQL czy nie
        db_vendor = connection.vendor  # 'postgresql', 'sqlite', 'mysql', itd.

        if db_vendor == 'postgresql':
            # PostgreSQL obsługuje JSONField contain -> filtrujemy normalnie
            for amenity in self.criteria.amenities:
                queryset = queryset.filter(amenities__contains=[amenity])
            return queryset
        else:
            # inne bazy (np. sqlite) -> filtrujemy ręcznie
            if not isinstance(queryset, list):
                queryset = list(queryset)

            return [
                prop for prop in queryset
                if all(amenity in prop.amenities for amenity in self.criteria.amenities)
            ]



class DistanceFilter(AbstractFilter):
    def __init__(self, criteria: DistanceCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if self.criteria.max_distance is not None:
            if isinstance(queryset, list):
                return [
                    prop for prop in queryset
                    if prop.distance_to_center <= self.criteria.max_distance
                ]
            else:
                return queryset.filter(distance_to_center__lte=self.criteria.max_distance)
        return queryset


class PropertyTypeFilter(AbstractFilter):
    def __init__(self, criteria: PropertyTypeCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if self.criteria.property_types:
            if isinstance(queryset, list):
                return [
                    prop for prop in queryset
                    if prop.property_type in self.criteria.property_types
                ]
            else:
                return queryset.filter(property_type__in=self.criteria.property_types)
        return queryset


class ReviewCountFilter(AbstractFilter):
    def __init__(self, criteria: ReviewCountCriteria):
        super().__init__()
        self.criteria = criteria

    def apply(self, queryset):
        if self.criteria.min_reviews is not None:
            if isinstance(queryset, list):
                return [
                    prop for prop in queryset
                    if prop.review_count >= self.criteria.min_reviews
                ]
            else:
                return queryset.filter(review_count__gte=self.criteria.min_reviews)
        return queryset
