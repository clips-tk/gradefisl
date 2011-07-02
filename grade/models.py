from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    capacity = models.IntegerField()
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    translation = models.BooleanField()

    def __unicode__(self):
        return unicode(self.name)


class Area(models.Model):
    description = models.TextField()
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.name)


class Author(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=200)
    candidate = models.IntegerField()

    def __unicode__(self):
        return unicode(self.name)


class Zone(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.name)


class Talk(models.Model):
    area = models.ForeignKey(Area)
    room = models.ForeignKey(Room)
    zone = models.ForeignKey(Zone)
    hour = models.CharField(max_length=2)
    title = models.CharField(max_length=200)
    date = models.DateField()
    abstract = models.TextField()
    level = models.CharField(max_length=150)
    authors = models.ManyToManyField('Author')
    minute = models.CharField(max_length=2)
    listeners = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.title)
