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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


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


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField("get_total_price")

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj: CartItem):
        return obj.quantity * obj.product.unit_price

    # def create(self, validated_data):
    #     cart_id = self.context["cart_id"]
    #     return CartItem.objects.create(cart_id=cart_id, **validated_data)


class AddCartItemSerializer(serializers.ModelSerializer):
    # product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given ID was found.")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField("get_total_price")

    def get_total_price(self, cart: Cart):
        return sum(
            [item.product.unit_price * item.quantity for item in cart.items.all()]
        )

    class Meta:
        model = Cart
        fields = ["id", "created_at", "items", "total_price"]


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
