from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from base.models import Product
from base.products import products
from base.serializers import ProductSerializer

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = Product.objects.create(
        user = user,
        title = 'Sample Name',
        price = 0,
        category = 'Sample Category',
        rating_count = 0,
        description = '', 
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(id=pk)
    product.title = data['title']
    product.price = data['price']
    product.category = data['category']
    product.rating_count = data['countInStock']
    product.description = data['description']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response('Product deleted.')

@api_view(['POST'])
def uploadImage(request): 
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(id = product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded.')
