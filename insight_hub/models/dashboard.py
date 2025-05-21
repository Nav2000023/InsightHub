from django.db import models
from django.contrib.auth.models import User
import uuid

class Dashboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="dashboards")  # User as ManyToOne field, not null
    title = models.CharField(max_length=200, null=False)  # Title, not null
    description = models.TextField(null=True, blank=True)  # Description, nullable
    is_public = models.BooleanField(default=False)  # Boolean field to specify public or not
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the time when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update on every save
    allowed_users = models.ManyToManyField(User, related_name="shared_dashboards", blank=True)
    likes = models.ManyToManyField(User, related_name='dashboard_like',blank=True)

    def __str__(self):
        return self.title

    def number_of_likes(self):
        a=self.likes.count()
        if a>1:
            return (str(a))
        elif a<1:
            return ("")
        else:
            return (str(a))