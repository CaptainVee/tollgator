from django.db import models
import uuid

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pkid = models.BigAutoField(primary_key=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


# class TrueFalse(models.Model):
#     boolean = models.BooleanField(default=False)

#     def __str__(self):
#         return self.boolean


class Currency(BaseModel):
    code = models.CharField(max_length=3, unique=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code
