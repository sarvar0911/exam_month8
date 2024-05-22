from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RequirementListCreateView, RequirementDetailView,
    FAQListCreateView, FAQDetailView,
    ContactListCreateView, TagViewSet,
    PublicationViewSet, PaperViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'publications', PublicationViewSet)
router.register(r'tags', TagViewSet)
router.register(r'papers', PaperViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('requirements/', RequirementListCreateView.as_view(), name='requirement-list-create'),
    path('requirements/<int:pk>/', RequirementDetailView.as_view(), name='requirement-detail'),
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
]

urlpatterns += router.urls
