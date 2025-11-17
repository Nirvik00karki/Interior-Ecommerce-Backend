from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Office, TeamMember, Award, Partner, Testimonial
from .serializers import (
    OfficeSerializer, TeamMemberSerializer, AwardSerializer,
    PartnerSerializer, TestimonialSerializer
)

CACHE_TIME = 60 * 5  # 5 minutes


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all().order_by("id")
    serializer_class = OfficeSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.select_related("office").order_by("order")
    serializer_class = TeamMemberSerializer


@method_decorator(cache_page(CACHE_TIME), name="list")
class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all().order_by("-date_received")
    serializer_class = AwardSerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by("name")
    serializer_class = PartnerSerializer


@method_decorator(cache_page(CACHE_TIME), name="list")
class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by("id")
    serializer_class = TestimonialSerializer
