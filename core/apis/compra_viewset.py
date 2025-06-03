from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.models import Compra
from core.serializers import CompraSerializer

class CompraViewSet(viewsets.ModelViewSet):
    serializer_class = CompraSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Compra.objects.all()
        return Compra.objects.filter(usuario=user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
