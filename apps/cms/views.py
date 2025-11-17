from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Page, HeroSlide, Methodology, FAQ
from .serializers import PageSerializer, HeroSlideSerializer, MethodologySerializer, FAQSerializer

CACHE_TIME = 300


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


@method_decorator(cache_page(CACHE_TIME), name="list")
class HeroSlideViewSet(viewsets.ModelViewSet):
    queryset = HeroSlide.objects.all().order_by("order")
    serializer_class = HeroSlideSerializer


class MethodologyViewSet(viewsets.ModelViewSet):
    queryset = Methodology.objects.all().order_by("order")
    serializer_class = MethodologySerializer


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all().order_by("order")
    serializer_class = FAQSerializer
