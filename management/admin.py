
from django.contrib import admin
from .models import AssistantModel
from django.contrib.admin.sites import AlreadyRegistered
@admin.register(AssistantModel)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')
    search_fields = ('name', 'id')
    readonly_fields = ('id', 'org_id', 'created_at', 'updated_at', 'slug')
    fieldsets = (
        (None, {
            'fields': ('id', 'org_id', 'name', 'slug', 'created_at', 'updated_at')
        }),
        ('Configuration', {
            'fields': ('voice', 'model', 'transcriber', 'first_message', 'first_message_mode', 'voicemail_message', 'end_call_message')
        }),
        ('Settings', {
            'fields': ('recording_enabled', 'hipaa_enabled', 'backchanneling_enabled', 'background_denoising_enabled', 'model_output_in_messages_enabled', 'is_server_url_secret_set')
        }),
        ('Timeouts and Limits', {
            'fields': ('silence_timeout_seconds', 'max_duration_seconds', 'num_words_to_interrupt_assistant')
        }),
        ('Messages and Phrases', {
            'fields': ('client_messages', 'server_messages', 'end_call_phrases')
        }),
        ('Other', {
            'fields': ('background_sound', 'voicemail_detection')
        }),
    )

    def has_add_permission(self, request):
        return False  # Disable adding new assistants through admin

try:
    admin.site.register(AssistantModel, AssistantAdmin)
except AlreadyRegistered:
    pass  # Model has already been registered