from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField(null=True)
    translation = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name)


#class Area(models.Model):
#    id = models.IntegerField(unique=True, primary_key=True)
#    description = models.TextField()
#    name = models.CharField(max_length=200)

#    def __unicode__(self):
#        return unicode(self.name)


class Author(models.Model):
    name = models.CharField(max_length=200)
    resume = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Zone(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.name)


class Talk(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    authors = models.ManyToManyField('Author')
    room = models.ForeignKey(Room)
    zone = models.ForeignKey(Zone)
    date = models.DateField()
    hour = models.CharField(max_length=2)
    minute = models.CharField(max_length=2)
    listeners = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.title)
