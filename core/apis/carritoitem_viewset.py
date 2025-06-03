from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Carrito, CarritoItem
from core.serializers import CarritoItemSerializer


class CarritoItemViewSet(viewsets.ModelViewSet):
    serializer_class = CarritoItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CarritoItem.objects.filter(carrito__usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        libro_id = request.data.get('libro_id')
        if not libro_id:
            return Response({'error': 'Se requiere libro_id'}, status=status.HTTP_400_BAD_REQUEST)

        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        if CarritoItem.objects.filter(carrito=carrito, libro_id=libro_id).exists():
            return Response({'error': 'El libro ya está en el carrito'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(carrito=carrito)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
