from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.catalog.models import ProductVariant

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add-item")
    def add_item(self, request):
        from apps.catalog.models import Inventory
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"error": "Invalid variant ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Check stock availability
        inv = Inventory.objects.filter(variant=variant).first()
        if not inv:
            return Response({"error": "Inventory not found for this product"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get existing cart quantity if adding to existing item
        cart_item = CartItem.objects.filter(cart=cart, variant=variant).first()
        existing_quantity = cart_item.quantity if cart_item else 0
        total_quantity = existing_quantity + quantity
        
        if inv.available_stock < total_quantity:
            return Response({
                "error": f"Insufficient stock. Available: {inv.available_stock}, Requested: {total_quantity}"
            }, status=status.HTTP_400_BAD_REQUEST)

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart=cart, variant=variant, quantity=quantity)
        
        cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="update-item")
    def update_item(self, request):
        from apps.catalog.models import Inventory
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            cart_item = CartItem.objects.get(cart=cart, variant_id=variant_id)
            
            if quantity > 0:
                # Check stock before updating
                inv = Inventory.objects.filter(variant=cart_item.variant).first()
                if inv and inv.available_stock < quantity:
                    return Response({
                        "error": f"Insufficient stock. Available: {inv.available_stock}"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({"error": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)

        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"], url_path="remove-item")
    def remove_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        variant_id = request.data.get("variant_id")

        CartItem.objects.filter(cart=cart, variant_id=variant_id).delete()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"], url_path="clear")
    def clear_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)
