

# Create your models here.
from django.db import models
from django.utils.text import slugify
#this is a assistant model for saving to the db
class Assistant(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    org_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    voice = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True,null=True)
    updated_at = models.DateTimeField(blank=True,null=True)
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
    slug = models.SlugField(
        max_length=255,  # Maximum length of the slug
        unique=True,  # Ensure each slug is unique
        blank=True,  # Allow the field to be blank
        null=True,  # Allow the field to be null in the database
        db_index=True,  # Add a database index for faster lookups
        allow_unicode=False,  # Restrict to ASCII-only characters
        help_text="Unique URL-friendly identifier automatically generated from the id"
    )
    def __str__(self):
        return f"name={self.name}, created_at={self.created_at})"
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Automatically generate slug from name if slug is not set
            self.slug = slugify(self.id)
        super(Assistant, self).save(*args, **kwargs)