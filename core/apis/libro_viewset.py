from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from core.models import Libro
from core.serializers import LibroSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'top_10']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def top_10(self, request):
        top_libros = Libro.objects.order_by('-ventas')[:10]
        serializer = self.get_serializer(top_libros, many=True)
        return Response(serializer.data)
