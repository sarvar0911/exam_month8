from django.urls import path
from .views import (RequirementListCreateView, RequirementDetailView,
                    FAQListCreateView, FAQDetailView,
                    ContactListCreateView)

urlpatterns = [
    path('requirements/', RequirementListCreateView.as_view(), name='requirement-list-create'),
    path('requirements/<int:pk>/', RequirementDetailView.as_view(), name='requirement-detail'),

    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),

    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
]
