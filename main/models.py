from django.db import models
from accounts.models import User


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag Name')

    def __str__(self):
        return self.name


class Requirement(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.title


class FAQ(AbstractBaseModel):
    question = models.CharField(max_length=255, verbose_name='Question')
    answer = models.TextField(verbose_name='Answer')

    def __str__(self):
        return self.question


class Contact(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')

    def __str__(self):
        return f'Contact from {self.first_name} - {self.email}'


class Publication(AbstractBaseModel):
    title_uz = models.CharField(max_length=255, verbose_name='Title (UZ)', null=True)
    title_en = models.CharField(max_length=255, verbose_name='Title (EN)')
    description_uz = models.TextField(verbose_name='Description (UZ)', null=True)
    description_en = models.TextField(verbose_name='Description (EN)')
    file = models.FileField(upload_to='publications/', verbose_name='File')
    image = models.ImageField(upload_to='publications/', verbose_name='Image')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')

    def __str__(self):
        return self.title_en


class Paper(AbstractBaseModel):
    title_uz = models.CharField(max_length=255, verbose_name='Title (UZ)', null=True)
    title_en = models.CharField(max_length=255, verbose_name='Title (EN)')
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    description_uz = models.TextField(verbose_name='Description (UZ)', null=True)
    description_en = models.TextField(verbose_name='Description (EN)')
    file = models.FileField(upload_to='papers/', verbose_name='File')
    keywords_uz = models.CharField(max_length=255, verbose_name='Keywords (UZ)', null=True)
    keywords_en = models.CharField(max_length=255, verbose_name='Keywords (EN)')
    article_uz = models.TextField(verbose_name='Article (UZ)', null=True)
    article_en = models.TextField(verbose_name='Article (EN)')
    views = models.PositiveIntegerField(default=0, verbose_name='Views')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Publication')

    def __str__(self):
        return self.title_en


class Review(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='reviews', verbose_name='Paper')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Reviewer')
    content = models.FileField(upload_to='reviews/', verbose_name='Content')

    def __str__(self):
        return f'Review by {self.reviewer} on {self.paper}'
