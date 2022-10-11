from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Blogs(models.Model):
    title=models.CharField(max_length=56)
    content = models.CharField(max_length=56)
    author = models.CharField(max_length=50)
    liked_by = models.CharField(max_length=56)

    def __str__(self):  # (self ==> current object (Blogs) )
        return self.title

class Mobiles(models.Model):
    name=models.CharField(max_length=120,unique=True)
    price=models.PositiveIntegerField(default=5000)
    band=models.CharField(max_length=100,default="4g")
    display=models.CharField(max_length=120)
    processor=models.CharField(max_length=120)

    def __str__(self):
        return self.name
    def average_rating(self): #self means one mobile object.
        reviews=self.reviews_set.all()
        if reviews:
            rating=[rv.rating for rv in reviews]
            total=sum(rating)
            return total/len(reviews)
        else:
            return 0
    def total_reviews(self):
        return self.reviews_set.all().count()

class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE) #CASCADE kazhinjitt () venda
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    review=models.CharField(max_length=150)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    date=models.DateField(auto_now_add=True)

    class Meta:
        unique_together=("author","product")

    def __str__(self):
        return self.review

class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
        ("incart","incart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=100,choices=options,default="incart")

class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Mobiles, on_delete=models.CASCADE)
    options=(
        ("order-placed", "order-placed"),
        ("dispatched","dispatched"),
        ("cancelled", "cancelled"),
        ("in-transit", "in-transit"),
        ("delivered", "delivered")
    )
    status=models.CharField(max_length=100,choices=options,default="order-placed")





# orm(object relational mapping) query for creating resourse
# modelname.objects.create(field1=value1,field2=value2,field3=value3,..)  (modelname means class name)
# Blogs.objects.create(title="goodmorning",content="hai",

# orm query for fetching all objects
# variablename=modelname.objects.all()
# qs=Blogs.objects.all()

# orm query for fetching detail view of a specific object(oru object mathre return cheyyu)
# variablename=modelname.objects.get(id=1)
# blog=Blogs.objects.get(id=1)

# filter()
# variablename=modelname.objects.filter(band="4g")  ("not equal to" illa, athinu pakaram aanu exclude)
# "4g" band ulla ella mobiles return cheyyan

# variablename=modelname.objects.filter(price__lt=2000)  (__gt=  __gte=   __lt=   __lte=)
# price less than 2000 ulla mobiles return cheyyan

# exclude()
# variablename=modelname.objects.all().exclude(band="5g")

# if 2 conditions to filter
#  qs=Mobiles.objects.filter(price__lt=25000,band="5G")

# count()
# 4g mobiles nte count


# print all mobiles price less than 32000

# query set aayitt aanu nammakk database lott kittuka
# ath client nu manassilavilla
# so convert it into list of dic, or whatever
# then to jason file
# similarly viceversa


