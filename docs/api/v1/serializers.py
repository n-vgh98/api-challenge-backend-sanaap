from rest_framework import serializers
from docs.models import FileObject


class FileSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FileObject
        fields = ["id", "file_name", "file_url", "updated_at", "created_at", "author"]
        read_only_fields = ["id", "file_name", "file_url", "updated_at", "created_at", "author"]
