from rest_framework import serializers
from .models import Collection, Product, Review, Cart, CartItem, OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):
    collection_url = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="collection-detail",  # Replace with your view name
        lookup_field="pk",
        source="collection",
    )
    collection = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "inventory",
            "unit_price",
            "collection",
            "collection_url",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "product_count",
        ]

    product_count = serializers.SerializerMethodField(method_name="ProductCount")

    def ProductCount(self, collection: Collection):
        return collection.products.count()


class CartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartitemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "created_at", "items"]


class ReviewSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.SerializerMethodField("get_customer_first_name")

    class Meta:
        model = Review
        fields = ["id", "date", "description", "customer_first_name"]

    def get_customer_first_name(self, obj: Review):
        customer = obj.customer
        return customer.first_name

    def create(self, validated_data):
        product_id = self.context["product_id"]
        customer = self.context["customer"]
        return Review.objects.create(
            product_id=product_id, customer=customer, **validated_data
        )
