from rest_framework import viewsets, permissions
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
from .models import Page, HeroSlide, Methodology, FAQ
from .serializers import PageSerializer, HeroSlideSerializer, MethodologySerializer, FAQSerializer

CACHE_TIME = 300


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    # Pages are publicly readable; editing requires authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    

    @action(detail=False, methods=["get"], url_path="slug/(?P<slug>[^/.]+)")
    def retrieve_by_slug(self, request, slug=None):
        page = get_object_or_404(Page, slug=slug)
        serializer = self.get_serializer(page)
        return Response(serializer.data)


# @method_decorator(cache_page(CACHE_TIME), name="list")
class HeroSlideViewSet(viewsets.ModelViewSet):
    queryset = HeroSlide.objects.all().order_by("order")
    serializer_class = HeroSlideSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    


class MethodologyViewSet(viewsets.ModelViewSet):
    queryset = Methodology.objects.all().order_by("order")
    serializer_class = MethodologySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all().order_by("order")
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
