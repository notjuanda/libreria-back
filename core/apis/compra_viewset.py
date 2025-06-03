import json
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from core.models import Compra
from core.serializers import CompraSerializer

class CompraViewSet(viewsets.ModelViewSet):
    serializer_class = CompraSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Compra.objects.all()
        return Compra.objects.filter(usuario=user)

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        if 'detalles' in data and isinstance(data['detalles'], str):
            try:
                data['detalles'] = json.loads(data['detalles'])
            except Exception:
                return Response(
                    {"detalles": ["Formato JSON inválido."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
