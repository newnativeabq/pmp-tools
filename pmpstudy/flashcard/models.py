from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from tagging.registry import register

# Create your models here.
class FlashCard(models.Model):
    title = models.CharField(max_length=100)
    frontface = models.TextField()
    backface = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    activated = models.BooleanField(blank=True, null=True)
    owner = models.ForeignKey('auth.User', on_delete='CASCADE', default=None)
    know_level = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
            ]
        )

    def activate_card(self):
        self.activated = True

    def deactivate_card(self):
        self.activated = False

    def get_absolute_url(self):
        return reverse("card_detail", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

register(FlashCard)