from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class CSVImport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.csv_file.name
