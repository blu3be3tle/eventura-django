from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.jpg'
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+8809999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
