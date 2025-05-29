from django.contrib import admin

from newsletters.models import Recipient, Message, Distribution


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name')
    search_fields = ('email', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme')
    search_fields = ('theme',)

@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'message')
    search_fields = ('status', )
