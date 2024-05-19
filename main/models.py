from django.db import models

from accounts.models import User


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Publication(AbstractBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='publications/')
    image = models.ImageField(upload_to='publications/')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Paper(AbstractBaseModel):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='papers/')
    keywords = models.CharField(max_length=255)
    article = models.TextField()
    tags = models.ManyToManyField(Tag)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'Review by {self.reviewer} on {self.paper}'


class Requirement(AbstractBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()


class FAQ(AbstractBaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'Contact from {self.first_name} - {self.email}'
