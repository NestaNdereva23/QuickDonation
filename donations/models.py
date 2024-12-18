from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField
import uuid
# Create your models here.
class Organizations(models.Model):

    organization_name = models.CharField(max_length=123)
    location = models.CharField(max_length=123)
    description = models.TextField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.organization_name}'

class Donation(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Donation from {self.phone_number}"



# STATUS = ((1, "Pending"), (0, "Complete"))

# class Transaction(models.Model):
#     '''This model records all the mpesa payment transactions'''

#     transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
#     phone_number = PhoneNumberField(null=False, blank=False)
#     checkout_request_id = models.CharField(max_length=200)
#     reference = models.CharField(max_length=40, blank=True)
#     description = models.TextField(null=True, blank=True)
#     amount = models.CharField(max_length=10)
#     status = models.CharField(max_length=15, choices=STATUS, default=1)
#     receipt_no = models.CharField(max_length=200, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     ip = models.CharField(max_length=200, blank=True, null=True)

#     def __unicode__(self):
#         return f"{self.transaction_no}"
