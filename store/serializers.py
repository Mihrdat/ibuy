from rest_framework import serializers
from .models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'title',
            'products_count',
        ]


class ProductSerializer(serializers.ModelSerializer):
    collection_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'inventory',
            'last_update',
            'unit_price',
            'collection_id',
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'unit_price',
        ]
