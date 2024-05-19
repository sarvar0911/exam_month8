from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import Requirement, FAQ, Contact
from .serializers import RequirementSerializer, FAQSerializer, ContactSerializer


class RequirementListCreateView(generics.ListCreateAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Only admins can create, update, or delete
        else:
            self.permission_classes = [AllowAny]  # Everyone can view for now, then I will change it to isAuthenticated
        return super().get_permissions()


class RequirementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = [IsAdminUser]  # Only admins can update or delete


class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Only admins can create, update, or delete
        else:
            self.permission_classes = [AllowAny]  # Everyone can view for now, then I will change it to isAuthenticated
        return super().get_permissions()


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Only admins can update or delete
        else:
            self.permission_classes = [AllowAny]  # Everyone can view for now, then I will change it to isAuthenticated
        return super().get_permissions()


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]  # Everyone can create for now, then I will change it to isAuthenticated

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
        if self.request.method in ['POST']:
            self.permission_classes = [AllowAny]  # Everyone can create for now, then I'll change it to isAuthenticated
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
