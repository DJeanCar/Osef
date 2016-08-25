from django.db import models
from django.utils import timezone

class TimeStamp(models.Model):

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

	class Meta:
		abstract = True