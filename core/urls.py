from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.apis import (
    UserViewSet,
    GeneroViewSet,
    LibroViewSet,
    CarritoViewSet,
    CarritoItemViewSet,
    CompraViewSet,
)
from core.apis.auth_viewset import AuthViewSet

router = DefaultRouter()
router.register('usuarios', UserViewSet, basename='usuarios')
router.register('generos', GeneroViewSet, basename='generos')
router.register('libros', LibroViewSet, basename='libros')
router.register('carritos', CarritoViewSet, basename='carritos')
router.register('carrito-items', CarritoItemViewSet, basename='carrito-items')
router.register('compras', CompraViewSet, basename='compras')
router.register('auth', AuthViewSet, basename='auth')


urlpatterns = [
    path('', include(router.urls)),
]
