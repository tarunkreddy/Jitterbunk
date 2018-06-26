

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    userprofile = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='profilePics/', default='default-profile-picture.png')
    def __str__(self):
        return self.user
class Bunk(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='bunkUser', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    time = models.DateTimeField('time of bunk')
    def __str__(self):
        return (str(self.from_user) + " --> " + str(self.to_user))

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(userprofile=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

