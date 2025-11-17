from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from docs.models import FileObject
from docs.api.v1.serializers import FileSerializer
from accounts.permissions import AdminEditorCanWrite
from config.minio_settings import upload_file_to_minio, delete_from_minio


class FileListCreateView(generics.ListCreateAPIView):
    queryset = FileObject.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, AdminEditorCanWrite]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username', 'created_at']
    search_fields = ['file_name']
    ordering_fields = ['created_at', 'file_name']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        file = self.request.FILES["file"]
        file_name, file_url = upload_file_to_minio(file, file.content_type)
        serializer.save(owner=self.request.user, file_name=file_name, file_url=file_url)


class FileDetailView(generics.RetrieveDestroyAPIView):
    queryset = FileObject.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, AdminEditorCanWrite]

    def perform_destroy(self, instance):
        deleted = delete_from_minio(instance.file_name)
        if not deleted:
            print("Warning: file not found in MinIO")
        instance.delete()
