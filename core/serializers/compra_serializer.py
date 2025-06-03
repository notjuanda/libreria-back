from rest_framework import serializers
from core.models import Compra, DetalleCompra, Libro
from core.serializers.libro_serializer import LibroSerializer


class DetalleCompraSerializer(serializers.ModelSerializer):
    libro = LibroSerializer(read_only=True)
    libro_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Libro.objects.all(), source='libro')

    class Meta:
        model = DetalleCompra
        fields = ['id', 'libro', 'libro_id', 'cantidad']

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(source='detallecompra_set', many=True)
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Compra
        fields = ['id', 'usuario', 'monto_total', 'comprobante_pago', 'qr', 'fecha', 'estado', 'detalles']
        read_only_fields = ['usuario', 'fecha', 'estado']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detallecompra_set')
        compra = Compra.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleCompra.objects.create(compra=compra, **detalle_data)
        return compra

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detallecompra_set', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if detalles_data is not None:
            instance.detallecompra_set.all().delete()
            for detalle_data in detalles_data:
                DetalleCompra.objects.create(compra=instance, **detalle_data)

        return instance
