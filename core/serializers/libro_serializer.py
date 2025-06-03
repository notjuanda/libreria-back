from rest_framework import serializers
from core.models import Libro, Genero
from core.serializers.genero_serializer import GeneroSerializer


class LibroSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)  # Mostrar info de géneros
    generos_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Genero.objects.all(), source='generos'
    )

    class Meta:
        model = Libro
        fields = ['id', 'foto', 'nombre', 'autor', 'precio', 'isbn', 'descripcion', 'generos', 'generos_ids', 'ventas']

    def create(self, validated_data):
        generos = validated_data.pop('generos')
        libro = Libro.objects.create(**validated_data)
        libro.generos.set(generos)
        return libro

    def update(self, instance, validated_data):
        generos = validated_data.pop('generos', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if generos is not None:
            instance.generos.set(generos)
        instance.save()
        return instance
