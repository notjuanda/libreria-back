from django.db import models

class Libro(models.Model):
    foto = models.ImageField(upload_to='libros/')
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    isbn = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField()
    generos = models.ManyToManyField('Genero', related_name='libros')
    ventas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
