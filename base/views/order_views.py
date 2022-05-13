from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import OrderSerializer
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail' : 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        # Create order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice'],
        )
        # Create shipping address
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'],
        )
        # Create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(id = i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.title,
                qty = i['qty'],
                price = i['price'],
                image = product.image.url,
            )
        # Update stock
            product.rating_count -= item.qty
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
