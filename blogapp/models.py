from django.db import models
from django.contrib.auth.models import User

class Blogs(models.Model):
    CATEGORY_CHOICES = [
        ("Technology", "Technology"),
        ("Design", "Design"),
        ("Lifestyle", "Lifestyle"),
        ("Travel", "Travel"),
        ("Food", "Food"),
        ("Science", "Science"),
    ]

    title = models.CharField(max_length=100)
    body  = models.TextField()
    blog_images = models.ImageField(upload_to= 'images/')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User ,on_delete= models.CASCADE)
    
    liked_by = models.ManyToManyField(User,related_name="liked_blogs",blank=True)

    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,default="Technology")

    @property
    def likes_count(self):
        return self.liked_by.count()

    def __str__(self):
        return self.title[:50]


class Comment(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

  
