from django.db import models

class book(models.Model):
    book_name=models.CharField(max_length=120)
    author=models.CharField(max_length=120)
    price=models.IntegerField()
    publisher=models.CharField(max_length=120)
    quantity=models.IntegerField()