# hosts/views.py
from rest_framework import viewsets, filters
from .models import Host
from .models import HostBooking
from .models import HostAvailability
from .models import HostMessage
from .models import HostPromotion
from .models import HostStatistics
from .models import HostEarnings
from .models import HostReservationPolicy
from .models import HostNotification
from .models import HostSupport
from .models import HostManager
from .models import HostProfile
from .models import HostFeedback
from .models import IndividualHost
from .models import CorporateHost
from .models import HostRating
from .models import HostReview
from .serializers import HostSerializer
from .serializers import HostAvailability
from .serializers import HostAvailabilitySerializer
from .serializers import HostBookingSerializer
from .serializers import HostMessageSerializer
from .serializers import HostPromotionSerializer
from .serializers import HostStatisticsSerializer
from .serializers import HostEarningsSerializer
from .serializers import HostReservationPolicySerializer
from .serializers import HostNotificationSerializer
from .serializers import HostSupportSerializer
from .serializers import HostManagerSerializer
from .serializers import HostProfileSerializer
from .serializers import HostFeedbackSerializer
from .serializers import IndividualHostSerializer
from .serializers import CorporateHostSerializer
from .serializers import HostRatingSerializer
from .serializers import HostReviewSerializer

class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['location']

class HostAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = HostAvailability.objects.all()
    serializer_class = HostAvailabilitySerializer

class HostBookingViewSet(viewsets.ModelViewSet):
    queryset = HostBooking.objects.all()
    serializer_class = HostBookingSerializer

class HostMessageViewSet(viewsets.ModelViewSet):
    queryset = HostMessage.objects.all()
    serializer_class = HostMessageSerializer

class HostPromotionViewSet(viewsets.ModelViewSet):
    queryset = HostPromotion.objects.all()
    serializer_class = HostPromotionSerializer

class HostStatisticsViewSet(viewsets.ModelViewSet):
    queryset = HostStatistics.objects.all()
    serializer_class = HostStatisticsSerializer

class HostEarningsViewSet(viewsets.ModelViewSet):
    queryset = HostEarnings.objects.all()
    serializer_class = HostEarningsSerializer

class HostReservationPolicyViewSet(viewsets.ModelViewSet):
    queryset = HostReservationPolicy.objects.all()
    serializer_class = HostReservationPolicySerializer


class HostNotificationViewSet(viewsets.ModelViewSet):
    queryset = HostNotification.objects.all()
    serializer_class = HostNotificationSerializer

class HostSupportViewSet(viewsets.ModelViewSet):
    queryset = HostSupport.objects.all()
    serializer_class = HostSupportSerializer

class HostManagerViewSet(viewsets.ModelViewSet):
    queryset = HostManager.objects.all()
    serializer_class = HostManagerSerializer

class HostProfileViewSet(viewsets.ModelViewSet):
    queryset = HostProfile.objects.all()
    serializer_class = HostProfileSerializer

class HostFeedbackViewSet(viewsets.ModelViewSet):
    queryset = HostFeedback.objects.all()
    serializer_class = HostFeedbackSerializer

class IndividualHostViewSet(viewsets.ModelViewSet):
    queryset = IndividualHost.objects.all()
    serializer_class = IndividualHostSerializer

class CorporateHostViewSet(viewsets.ModelViewSet):
    queryset = CorporateHost.objects.all()
    serializer_class = CorporateHostSerializer

class HostRatingViewSet(viewsets.ModelViewSet):
    queryset = HostRating.objects.all()
    serializer_class = HostRatingSerializer

class HostReviewViewSet(viewsets.ModelViewSet):
    queryset = HostReview.objects.all()
    serializer_class = HostReviewSerializer