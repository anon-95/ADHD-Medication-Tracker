from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from .utils import calculate_streak
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = "default.jpg", upload_to= "profile_pics/")
    medication = models.CharField(default="not chosen", max_length=100)
    dosage = models.IntegerField(default=0)
    start_date = models.DateField(default=timezone.now)
    streak = models.IntegerField(default=0)

    def update_streak(self):
        self.streak = calculate_streak(self.user, self.streak)
        self.save()

    def __str__(self):
        return f"{self.user} Profile"
    def save(self, *args, **kwargs):

                # Check if the image has been updated (i.e., if it's not the default image)
        if self.pk:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.image != self.image:
                # If the image is being updated, delete the old image
                old_image_path = old_profile.image.path
                if os.path.isfile(old_image_path) and old_profile.image != 'profile_pics/default.jpg':
                    os.remove(old_image_path)
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)            
            img.save(self.image.path)

