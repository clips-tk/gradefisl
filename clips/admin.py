# -*- coding: utf-8 -*-

from django.contrib import admin
from clips.models import Talk
from clips.models import Room
from clips.models import Author
from clips.models import Zone


class TalkAdmin(admin.ModelAdmin):
    fields = ['title', 'abstract', 'date', 'authors', 'zone', 'room', 'language']
    list_display = ('title', 'date', 'zone', 'room')
    list_filter = ['date', 'zone', 'room', 'language']
    search_fields = ('title', 'abstract', 'authors')


class AuthorAdmin(admin.ModelAdmin):
    fields = ['name', 'bio']
    list_display = ('name',)
    search_fields = ('name',)


class RoomAdmin(admin.ModelAdmin):
    fields = ['name', 'capacity', 'translation']
    search_fields = ('name',)


class ZoneAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Talk, TalkAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Zone, ZoneAdmin)
