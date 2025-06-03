from django.db import models
from django.conf import settings

class Compra(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libros = models.ManyToManyField('Libro', through='DetalleCompra')
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    comprobante_pago = models.ImageField(upload_to='comprobantes/', null=True, blank=True)
    qr = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username} - {self.estado}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.libro.nombre} x {self.cantidad}"
