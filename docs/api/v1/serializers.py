from rest_framework import serializers
from django.urls import reverse
from docs.models import FileObject


class FileSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    download_url = serializers.SerializerMethodField()

    class FileSerializer(serializers.ModelSerializer):
        class Meta:
            model = FileObject
            fields = ["id", "file_name", "file_url", "uploaded_at", "author"]
            read_only_fields = ["id", "file_name", "file_url", "uploaded_at", "author"]