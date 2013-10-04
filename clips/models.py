from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=200, unique=True)
    capacity = models.IntegerField(null=True, blank=True)
    translation = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name)


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Zone(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Talk(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    authors = models.ManyToManyField('Author')
    room = models.ForeignKey(Room)
    zone = models.ForeignKey(Zone)
    language = models.CharField(max_length=5, null=True, blank=True)
    listeners = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.title)
