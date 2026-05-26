from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProductView(models.Model):
    product = models.ForeignKey(Product, related_name='views', on_delete=models.CASCADE)
    view_name = models.CharField(max_length=100, help_text="e.g., Front, Back, Side")
    base_image = models.ImageField(upload_to='products/base_images/')
    
    # Print Area coordinates (rectangle)
    print_area_x = models.IntegerField(help_text="X coordinate of top-left corner")
    print_area_y = models.IntegerField(help_text="Y coordinate of top-left corner")
    print_area_width = models.IntegerField(help_text="Width of print area")
    print_area_height = models.IntegerField(help_text="Height of print area")

    def __str__(self):
        return f"{self.product.name} - {self.view_name}"

class Design(models.Model):
    image = models.ImageField(upload_to='designs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Design {self.id}"

class RenderJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    product_view = models.ForeignKey(ProductView, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_image = models.ImageField(upload_to='results/', null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job {self.id} - {self.status}"

