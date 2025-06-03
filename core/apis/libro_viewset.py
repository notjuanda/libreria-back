from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from core.models import Libro, Genero
from core.serializers import LibroSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'top_10', 'por_genero']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def top_10(self, request):
        top_libros = Libro.objects.order_by('-ventas')[:10]
        serializer = self.get_serializer(top_libros, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='por-genero/(?P<genero_id>[^/.]+)')
    def por_genero(self, request, genero_id=None):
        try:
            genero = Genero.objects.get(pk=genero_id)
        except Genero.DoesNotExist:
            return Response({"error": "Género no encontrado"}, status=404)

        libros = self.queryset.filter(generos=genero)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)