from rest_framework import serializers

from django.db import transaction
from django.contrib.auth import get_user_model

from .models import (
    Collection,
    Product,
    Cart,
    CartItem,
    Customer,
    Order,
    OrderItem,
    ProductImage,
    Review,
)


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'title',
            'products_count',
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    collection_id = serializers.IntegerField()
    images = ProductImageSerializer(many=True, read_only=True)

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
            'images',
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'unit_price',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity',
            'total_price',
        ]

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product_id',
            'quantity',
        ]

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_price',
        ]


class CustomerSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'phone',
            'birth_date',
            'user',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'unit_price',
        ]


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    items = OrderItemSerializer(many=True)
    invoice_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'placed_at',
            'customer',
            'items',
            'invoice_amount',
        ]

    def get_invoice_amount(self, order):
        return sum([item.quantity * item.unit_price for item in order.items.all()])


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    @transaction.atomic()
    def create(self, validated_data):
        cart_id = validated_data['cart_id']
        customer = Customer.objects.get(user=self.context['user'])
        order = Order.objects.create(customer=customer)

        cart_items = CartItem.objects \
                             .filter(cart_id=cart_id) \
                             .select_related('product')

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.unit_price
            ) for item in cart_items
        ]

        OrderItem.objects.bulk_create(order_items)
        Cart.objects.filter(pk=cart_id).delete()

        return order


class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'description',
            'date',
            'user',
        ]

    def create(self, validated_data):
        product_id = self.context['product_id']
        user = self.context['user']
        return Review.objects.create(product_id=product_id, user=user, **validated_data)
