from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.views.decorators.cache import cache_page
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Office, TeamMember, Award, Partner, Testimonial, SocialMedia
from .serializers import (
    OfficeSerializer, TeamMemberSerializer, AwardSerializer,
    PartnerSerializer, TestimonialSerializer, SocialMediaSerializer
)

CACHE_TIME = 60 * 5  # 5 minutes


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by("name")
    serializer_class = PartnerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=["get"], url_path="slug/(?P<slug>[^/.]+)")
    def retrieve_by_slug(self, request, slug=None):
        partner = get_object_or_404(Partner, slug=slug)
        serializer = self.get_serializer(partner)
        return Response(serializer.data)


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all().order_by("id")
    serializer_class = OfficeSerializer
    # Offices should be publicly readable; editing requires authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.select_related("office").order_by("order")
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    


@method_decorator(cache_page(CACHE_TIME), name="list")
class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all().order_by("-date_received")
    serializer_class = AwardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by("name")
    serializer_class = PartnerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]    
    

@method_decorator(cache_page(CACHE_TIME), name="list")
class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by("id")
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    
class SocialMediaViewSet(viewsets.ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
