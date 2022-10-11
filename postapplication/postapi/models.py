from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dob=models.DateField(null=True)
    options=(
        ("male","male"),
        ("female","female")
    )
    gender=models.CharField(max_length=50,choices=options)
    profile_pic=models.ImageField(upload_to="profilepics",null=True)
    bio=models.CharField(max_length=120,null=True)
    cover_pic = models.ImageField(upload_to="coverpics", null=True)
    followings=models.ManyToManyField(User,related_name="following")


class Posts(models.Model):
    title=models.CharField(max_length=120)
    content=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="liked_by")

    def __str__(self):
        return self.title
    def fetch_comments(self):
        return self.comments_set.all()

    def like_count(self):
        return self.liked_by.all().count()


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=150)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment