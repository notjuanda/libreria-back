from rest_framework import serializers
from core.models import Carrito, CarritoItem, Libro
from core.serializers.libro_serializer import LibroSerializer


class CarritoItemSerializer(serializers.ModelSerializer):
    libro = LibroSerializer(read_only=True)
    libro_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Libro.objects.all(), source='libro')

    class Meta:
        model = CarritoItem
        fields = ['id', 'libro', 'libro_id', 'cantidad']

class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True)

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'items']
        read_only_fields = ['usuario']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        carrito = Carrito.objects.create(**validated_data)
        for item_data in items_data:
            CarritoItem.objects.create(carrito=carrito, **item_data)
        return carrito

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.save()

        for item_data in items_data:
            libro = item_data.get('libro')
            cantidad = item_data.get('cantidad')
            carrito_item, created = CarritoItem.objects.update_or_create(
                carrito=instance,
                libro=libro,
                defaults={'cantidad': cantidad}
            )
        return instance
