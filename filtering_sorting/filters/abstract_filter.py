from abc import ABC, abstractmethod

# Abstrakcyjna klasa kryteriów
class Criteria(ABC):
    @abstractmethod
    def set_criteria(self, *args, **kwargs):
        pass

# Abstrakcyjna klasa filtru
class AbstractFilter(ABC):
    def __init__(self, filter_id=None):
        self.filter_id = filter_id

    @abstractmethod
    def apply(self, queryset):
        pass
