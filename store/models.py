from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10,decimal_places=2)
#     status = models.CharField(max_length=50,default='pending')
#     created_at= models.DateTimeField(null=True,blank=True) 
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     address = models.TextField(default="Not provided") 
#     payment_method = models.CharField(max_length=50, default="COD")
#     ordered_at = models.DateTimeField(auto_now_add=True)
    

#     def __str__(self):
#      return f"Order by {self.user.username} - {self.product.name} ({self.quantity})"

    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
 

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

# class OrderItem(models.Model):
#      order = models.ForeignKey(Order, on_delete=models.CASCADE)
#      product = models.ForeignKey(Product, on_delete=models.CASCADE)
#      quantity = models.PositiveIntegerField()
#      price = models.DecimalField(max_digits=10, decimal_places=2)
#      def __str__(self):
#         return self.product.name

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders",)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0,)
    status = models.CharField(max_length=50,default="pending",)
    address = models.TextField(default="Not provided",)
    payment_method = models.CharField(max_length=50,default="Card",)
    ordered_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items",)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name