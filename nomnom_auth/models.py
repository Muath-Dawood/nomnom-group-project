from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from PIL import Image
import os

class User(AbstractUser):
    """
    Custom User model that uses email as the primary identifier
    instead of a username.
    """
    username = None
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        # is instance new
        is_new_instance = self.pk is None

        # Retrieve the previous value of profile_pic if the instance exists
        if not is_new_instance:
            old_instance = User.objects.filter(pk=self.pk).first()
            old_profile_pic = old_instance.profile_pic if old_instance else None
        else:
            old_profile_pic = None

        # Call the original save method first to ensure a pk is generated
        super().save(*args, **kwargs)

        # if instance is new or if profile_pic is updated
        if is_new_instance or self.profile_pic != old_profile_pic:
            if self.profile_pic:
                img_path = self.profile_pic.path
                img = Image.open(img_path)
                target_width = 320

                if img.width > target_width:
                    ratio = target_width / float(img.width)
                    target_height = int(float(img.height) * ratio)
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    img.save(img_path)

                # Rename the file to include a unique identifier
                unique_name = f"{uuid.uuid4()}{os.path.splitext(img_path)[1]}"
                new_path = os.path.join(os.path.dirname(img_path), unique_name)
                os.rename(img_path, new_path)
                self.profile_pic.name = os.path.relpath(new_path, os.path.dirname(new_path)[:-13])
                super().save(*args, **kwargs)

    def __str__(self):
        return self.email
