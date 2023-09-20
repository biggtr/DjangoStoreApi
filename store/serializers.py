from rest_framework import serializers
from .models import Collection, Product


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
