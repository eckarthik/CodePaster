from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
SYNTAX_CHOICES = [('Python','Python'),('C','C'),('C++','C++'),('Java','Java'),('JavaScript','JavaScript'),
                  ('HTML','HTML'),('CSS','CSS'),('TypeScript','TypeScript'),('Rust','Rust'),('Kotlin','Kotlin'),
                  ('C#','C#'),('Perl','Perl'),('PHP','PHP'),('SCALA','SCALA'),('Swift','Swift'),('SQL','SQL'),
                  ('R','R'),('Golang','Golang'),('Ruby','Ruby')]
EXPIRY_CHOICES = [('10m','10m'),('30m','30m'),('1h','1h'),('3h','3h'),('6h','6h'),('Never','Never')]
class Paste(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True)
    content = models.TextField()
    syntax = models.CharField(choices=SYNTAX_CHOICES,max_length=20)
    expiry = models.CharField(choices=EXPIRY_CHOICES,max_length=20)
    views = models.PositiveIntegerField(default=0,)
    user = models.ForeignKey('auth.User',on_delete=models.SET_NULL,null=True)
    slug = models.CharField(max_length=10,blank=True)

    class Meta:
        ordering = ['created_at']

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    location = models.CharField(max_length=50,blank=True)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)





