from django.contrib import admin

from .models import AccessLog

# Register your models here.


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'card_id', 'door_name', 'access_granted', 'timestamp']
    list_filter = ['access_granted', 'door_name', 'timestamp']
    search_fields = ['card_id', 'door_name']
    readonly_fields = ['timestamp']
