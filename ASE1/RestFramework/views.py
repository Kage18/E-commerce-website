from rest_framework.views import APIView
from vendor.models import Product, Category
from django.http import Http404
from rest_framework.response import Response
from vendor.serializers import ProductSerializer
from rest_framework import status


class ProductsList(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = ProductSerializer( data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get_products(self, pk):
        try:
            return Product.objects.filter(category=Category.objects.get(pk=pk))
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


