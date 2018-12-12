from rest_framework import serializers
from cart.models import Order, OrderItem


class OrderitemsSerializer(serializers.ModelSerializer):
    product=serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        # fields = ['product']
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    # items = serializers.StringRelatedField(many=True)
    items = OrderitemsSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
