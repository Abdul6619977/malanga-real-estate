from django.db import models

class Property(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    )
    TYPE_CHOICES = (
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Commercial', 'Commercial Center'),
        ('Plot', 'Plot / Land'),
    )
    name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='House')
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Property sale price")
    bedrooms = models.IntegerField(null=True, blank=True, help_text="Number of bedrooms (if applicable)")
    bathrooms = models.IntegerField(null=True, blank=True, help_text="Number of bathrooms (if applicable)")
    size_sqm = models.IntegerField(null=True, blank=True, help_text="Size in square meters")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='properties/', null=True, blank=True)
    features = models.TextField(help_text="Comma-separated features", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Properties'

    def get_features_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.split(',') if f.strip()]

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Negotiating', 'Negotiating'),
        ('Sold', 'Sold'),
        ('Closed', 'Closed'),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry for {self.property.name} from {self.customer_name} ({self.status})"
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.name}"
