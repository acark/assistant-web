
from django.contrib import admin
from .models import Assistant
class AssistantAdmin(admin.ModelAdmin):
    list_display = ('id', 'org_id', 'name', 'voice', 'created_at', 'updated_at', 'recording_enabled', 'transcriber')
    search_fields = ('id', 'org_id', 'name', 'voice', 'transcriber')
    list_filter = ('recording_enabled', 'is_server_url_secret_set')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('id', 'org_id', 'name', 'voice', 'model', 'recording_enabled', 'background_sound', 'is_server_url_secret_set')
        }),
        ('Messages', {
            'fields': ('first_message', 'voicemail_message', 'end_call_message')
        }),
        ('Transcription', {
            'fields': ('transcriber', 'client_messages', 'server_messages', 'end_call_phrases', 'num_words_to_interrupt_assistant')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

admin.site.register(Assistant, AssistantAdmin)