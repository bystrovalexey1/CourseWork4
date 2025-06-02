from django.contrib import admin

from newsletters.models import Recipient, Message, Distribution, NewslettersAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'owner')
    search_fields = ('email', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'owner')
    search_fields = ('theme',)

@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'message', 'owner')
    search_fields = ('status', )

@admin.register(NewslettersAttempt)
class NewslettersAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt_send_data', 'attempt_status', 'distribution')
    search_fields = ('attempt_status', )
