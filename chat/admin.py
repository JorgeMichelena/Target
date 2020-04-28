from django.contrib.gis import admin
from chat.models import Match, Message


class MessageInline(admin.TabularInline):
    model = Message


class MatchAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    list_display = ['pk', 'creation_date', 'chat_start', 'target1', 'target2']


admin.site.register(Match, MatchAdmin)
