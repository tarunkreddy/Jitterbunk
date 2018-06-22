

from django.db import models

class UserProfile(models.Model):
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

