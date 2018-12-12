from rest_framework import serializers
from cart.models import Order, OrderItem


class OrderitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = '__all__'
