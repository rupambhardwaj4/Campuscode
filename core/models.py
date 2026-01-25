from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, default='Student') 
    college = models.CharField(max_length=100, default='CampusCode Institute')
    streak = models.IntegerField(default=0)
    college_rank = models.IntegerField(default=0)
    global_rank = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)

    @property
    def xp_percentage(self):
        return min((self.xp / 2000) * 100, 100)

class Problem(models.Model):
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20)
    points = models.IntegerField(default=10)
    acceptance = models.CharField(max_length=10, default='0%')
    tags = models.CharField(max_length=200, blank=True)
    statement = models.TextField()
    input_fmt = models.TextField()
    output_fmt = models.TextField()
    constraints = models.TextField()
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)

class Contest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    prizes = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, default='Upcoming')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.IntegerField(default=0)

    @property
    def duration(self):
        diff = self.end_time - self.start_time
        hours = diff.seconds // 3600
        return f"{hours} Hours"

class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)