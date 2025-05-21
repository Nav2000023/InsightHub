from django.db import models
import uuid, os

def unique_csv_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}_{filename}.{ext}"
    return os.path.join("csv_files", filename)

class CSVFile(models.Model):
    chart = models.OneToOneField('Chart', on_delete=models.CASCADE, null=False, related_name="csv_file")
    file_path = models.FileField(upload_to=unique_csv_file_path, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSV File for {self.chart.title}"
