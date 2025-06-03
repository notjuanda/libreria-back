from django.db import models
from django.conf import settings

class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1) 
    class Meta:
        unique_together = ('carrito', 'libro')

    def __str__(self):
        return f"{self.libro.nombre} x {self.cantidad}"
