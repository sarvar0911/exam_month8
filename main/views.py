from time import time

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response

from .filters import PaperFilter
from .models import Requirement, FAQ, Contact, Tag, Publication, Paper, Review
from .permissions import IsReviewer
from .serializers import (
    RequirementSerializer, FAQSerializer, ContactSerializer,
    TagSerializer, PublicationSerializer, PaperSerializer, ReviewSerializer
)


class RequirementListCreateView(generics.ListCreateAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class RequirementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = [IsAdminUser]


class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save()
        send_mail(
            subject=f"New Contact Message from {contact.first_name}",
            message=contact.message,
            from_email=contact.email,
            recipient_list=[settings.DEFAULT_CONTACT_EMAIL],
            fail_silently=False,
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all().order_by('-created_at')
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_publication = Publication.objects.order_by('-created_at').first()
        if latest_publication:
            serializer = PublicationSerializer(latest_publication)
            return Response(serializer.data)
        return Response({'detail': 'No publication found.'}, status=status.HTTP_404_NOT_FOUND)


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaperFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, pk=None, *args, **kwargs):
        title = f'Paper_{pk}'
        if title in request.COOKIES:
            if time() - float(request.COOKIES[title]) > 10:
                increment_view = True
            else:
                increment_view = False
        else:
            increment_view = True

        if increment_view:
            paper = Paper.objects.get(pk=pk)
            paper.views += 1
            paper.save()

        response = super().retrieve(request, pk=pk, *args, **kwargs)
        response.set_cookie(title, time())
        return response

    @action(detail=False, methods=['get'])
    def most_viewed(self, request):
        papers = Paper.objects.all().order_by('-views')[:10]
        serializer = self.get_serializer(papers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recently_uploaded(self, request):
        papers = Paper.objects.all().order_by('-created_at')[:10]
        serializer = self.get_serializer(papers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def papers_with_reviews(self, request, pk=None):
        try:
            paper = Paper.objects.get(pk=pk)
        except Paper.DoesNotExist:
            raise NotFound('Paper not found')

        paper_serializer = PaperSerializer(paper)
        reviews = Review.objects.filter(paper=paper)
        review_serializer = ReviewSerializer(reviews, many=True)
        return Response({
            'paper': paper_serializer.data,
            'reviews': review_serializer.data,
        }, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewer]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
