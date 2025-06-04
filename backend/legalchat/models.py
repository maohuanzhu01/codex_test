from django.db import models
from django.contrib.postgres.fields import JSONField

class Organization(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MEMBER = 'member', 'Member'

class LegalDocument(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    metadata = JSONField(blank=True, null=True)
    vector_embedding = models.BinaryField()

class ChatSession(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    embedding = models.BinaryField()
    citations = JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

