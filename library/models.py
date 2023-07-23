from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.db.models.fields.files import ImageField, FileField
from io import BytesIO

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
 
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateTimeField(null=True, blank=True)
 
    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
