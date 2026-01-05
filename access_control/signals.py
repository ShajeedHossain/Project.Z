import os
import subprocess
from datetime import datetime

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import AccessLog

LOG_FILE = 'system_events.log'

@receiver(post_save, sender=AccessLog)
def log_access_create(sender, instance, created, **kwargs):
    if created:
        status = "GRANTED" if instance.access_granted else "DENIED"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] - CREATE: Access log created for card {instance.card_id}. Status: {status}.\n"
        
        try:
            subprocess.run(
                ['bash', '-c', f'echo "{log_message}" >> {LOG_FILE}'],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error writing to log file: {e}")

@receiver(post_delete, sender=AccessLog)
def log_access_delete(sender, instance, **kwargs):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] - DELETE: Access log (ID: {instance.id}) for card {instance.card_id} was deleted.\n"
    
    try:
        subprocess.run(
            ['bash', '-c', f'echo "{log_message}" >> {LOG_FILE}'],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error writing to log file: {e}")