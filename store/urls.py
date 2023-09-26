from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    ProductViewSet,
    CollectionViewSet,
    ReviewViewSet,
    CartViewSet,
    CartItemViewSet,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"collections", CollectionViewSet, basename="collection")
router.register(r"carts", CartViewSet, basename="cart")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
products_router.register("reviews", ReviewViewSet, basename="product-reviews")
carts_router.register("items", CartItemViewSet, basename="cart-item")
urlpatterns = router.urls + products_router.urls + carts_router.urls
