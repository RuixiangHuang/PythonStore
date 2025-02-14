from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from api.serializers import GoodsSerializer
from goods.models import Goods

@api_view(['GET','POST'])
def good_list(request):
    if request.method == 'GET':
        cache_key = 'good_list'
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("goods_list")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def good_detail(request, id):
    cache_key = f"good_detail_{id}"

    if request.method == 'GET':
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data);

        try:
            goods = Goods.objects.get(id=id)
        except Goods.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GoodsSerializer(goods)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)


    if request.method == 'PUT':
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'DELETE':
        goods.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)