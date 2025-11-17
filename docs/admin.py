from django.contrib import admin
from .models import FileObject

@admin.register(FileObject)
class FileObjectAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'author', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at', 'author')
    search_fields = ('file_name', 'author__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    list_editable = ('is_active',)
