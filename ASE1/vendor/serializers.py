from rest_framework import serializers
from vendor.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ('prod_name', 'category', 'brand', 'stock', 'cost')
        fields = '__all__'
    # def create(self, validated_data):
    #     category = validated_data.pop('category')
    #     pname = validated_data['prod_name']
    #     brand = validated_data['brand']
    #     cost = validated_data['cost']
    #     stock = validated_data['stock']
    #     product = Product.objects.create(category=category, prod_name=pname, brand=brand, stock=stock, cost=cost)
    #     return product
