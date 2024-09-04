

# Create your models here.
from django.db import models
from django.utils.text import slugify
#this is a assistant model for saving to the db

class AssistantModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    org_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    voice = models.JSONField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    model = models.JSONField()
    recording_enabled = models.BooleanField(default=True)
    first_message = models.TextField()
    transcriber = models.JSONField()
    silence_timeout_seconds = models.IntegerField()
    client_messages = models.JSONField()
    server_messages = models.JSONField()
    end_call_phrases = models.JSONField()
    hipaa_enabled = models.BooleanField(default=False)
    max_duration_seconds = models.IntegerField()
    background_sound = models.CharField(max_length=255)
    backchanneling_enabled = models.BooleanField(default=False)
    first_message_mode = models.CharField(max_length=255)
    voicemail_detection = models.JSONField()
    background_denoising_enabled = models.BooleanField(default=False)
    model_output_in_messages_enabled = models.BooleanField(default=False)
    is_server_url_secret_set = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    # Add the missing fields
    voicemail_message = models.TextField(blank=True, null=True)
    end_call_message = models.TextField(blank=True, null=True)
    num_words_to_interrupt_assistant = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        ordering = ['-created_at']