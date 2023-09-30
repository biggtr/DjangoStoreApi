from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import (
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Order, Product, Collection, OrderItem, Review, CartItem, Cart
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CreateOrderSerializer,
    OrderSerializer,
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    UpdateCartItemSerializer,
    UpdateOrderSerializer,
)

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"].count() > 0):
            return Response(
                {"error": "this Product cannot be deleted because its ordered"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collecion = get_object_or_404(Collection, pk=kwargs["pk"])
        if collecion.products.count() > 0:
            return Response(
                {"error": "this Collection cannot be deleted because it has products"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CartViewSet(
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["cart_id"] = self.kwargs["cart_pk"]
        return context


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs["product_pk"]
        context["customer"] = self.request.user
        return context


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        Customer = get_user_model()
        customer_id = Customer.objects.only("id").get(pk=user.id)
        return Order.objects.filter(customer_id=customer_id)
