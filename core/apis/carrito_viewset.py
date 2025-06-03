from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Carrito
from core.serializers import CarritoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Carrito.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        if Carrito.objects.filter(usuario=request.user).exists():
            return Response({'error': 'Ya tienes un carrito activo'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def eliminar_mi_carrito(self, request):
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            carrito.delete()
            return Response({'detail': 'Carrito eliminado.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No tienes carrito activo.'}, status=status.HTTP_404_NOT_FOUND)
