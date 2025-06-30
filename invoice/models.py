from django.db import models
from user.models import User
from django.utils import timezone


# Create your models here.
class Invoice(models.Model):
    STATUS_CHOICE = [
        ("draft", "Draft"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("sent", "Sent"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    invoice_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="draft")
    amount = models.DecimalField(decimal_places=2,max_digits=20)
    currency = models.CharField(max_length=20,default="USD")
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.client_name}"

    class Meta:
        ordering = ["-created_at"]
