from django.conf import settings
from django.db import models
from django.utils import timezone
import csv

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    csv_file = models.FileField(upload_to='csv_files/', blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def read_csv_data(self):
        with self._lock:
            data = []
            with open(self.csv_file.path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
            return data

    def filter_csv_data_by_name(self, name):
        with self._lock:
            data = self.read_csv_data()
            filtered_data = [row for row in data if row and row[1] == name]
            return filtered_data

    def get_first_five_columns(self):
        with self._lock:
            data = self.read_csv_data()
            first_five_columns = [row[:5] for row in data]
            return first_five_columns

    def __str__(self):
        return self.title
