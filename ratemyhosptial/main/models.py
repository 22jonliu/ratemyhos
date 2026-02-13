from django.db import models

class Tag(models.Model):
        name = models.CharField(max_length=100, unique=True)
        
        def __str__(self):
            return self.name
# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="projects")
    link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.title 
    

class Tag(models.Model):
        name = models.CharField(max_length=100, unique=True)

