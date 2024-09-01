from django.db import models

# Create your models here.
from django.db import models

#this is a assistant model for saving to the db
class Assistant(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    org_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    voice = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    model = models.CharField(max_length=255, blank=True, null=True)
    recording_enabled = models.BooleanField(default=False)
    first_message = models.TextField(blank=True, null=True)
    voicemail_message = models.TextField(blank=True, null=True)
    end_call_message = models.TextField(blank=True, null=True)
    transcriber = models.CharField(max_length=255, blank=True, null=True)
    client_messages = models.JSONField(blank=True, null=True)
    server_messages = models.JSONField(blank=True, null=True)
    end_call_phrases = models.JSONField(blank=True, null=True)
    num_words_to_interrupt_assistant = models.IntegerField(blank=True, null=True)
    background_sound = models.CharField(max_length=255, blank=True, null=True)
    is_server_url_secret_set = models.BooleanField(default=False)