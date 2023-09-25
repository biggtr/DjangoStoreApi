from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet, CartViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"collections", CollectionViewSet, basename="collection")
router.register(r"carts", CartViewSet, basename="cart")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", ReviewViewSet, basename="product-reviews")
urlpatterns = router.urls + products_router.urls
