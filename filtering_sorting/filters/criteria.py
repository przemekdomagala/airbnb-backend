from .abstract_filter import Criteria

class PriceCriteria(Criteria):
    def __init__(self):
        self.min_price = None
        self.max_price = None

    def set_criteria(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price

class LocationCriteria(Criteria):
    def __init__(self):
        self.location_id = None

    def set_criteria(self, location_id):
        self.location_id = location_id

class RatingCriteria(Criteria):
    def __init__(self):
        self.min_rating = None
        self.max_rating = None

    def set_criteria(self, min_rating, max_rating):
        self.min_rating = min_rating
        self.max_rating = max_rating

class AmenityCriteria(Criteria):
    def __init__(self):
        self.amenities = []

    def set_criteria(self, amenities):
        self.amenities = amenities

class DistanceCriteria(Criteria):
    def __init__(self):
        self.max_distance = None

    def set_criteria(self, max_distance):
        self.max_distance = max_distance

class PropertyTypeCriteria(Criteria):
    def __init__(self):
        self.property_types = []

    def set_criteria(self, property_types):
        self.property_types = property_types

class ReviewCountCriteria(Criteria):
    def __init__(self):
        self.min_reviews = None

    def set_criteria(self, min_reviews):
        self.min_reviews = min_reviews
