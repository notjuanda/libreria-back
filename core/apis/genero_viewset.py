from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from core.models import Genero
from core.serializers import GeneroSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
