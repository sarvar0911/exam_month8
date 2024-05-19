from django.contrib import admin
from main.models import Tag, Paper, Publication, Review, Requirement, Contact, FAQ

admin.site.register(Tag)
admin.site.register(Paper)
admin.site.register(Publication)
admin.site.register(FAQ)
admin.site.register(Requirement)
admin.site.register(Review)
admin.site.register(Contact)
