from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group



news = "NW"
article = "AR"
CHOISE = [(news, 'Новость'),
               (article,'Статья')]

class Author(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating =0
        comments_rating =0
        comments_posts_rating =0
        posts= Post.objects.filter(post_author=self)
        comments= Comment.objects.filter(comm_user=self.user)
        comments_posts=Comment.objects.filter(post__author=self)
        for p in posts:
            posts_rating += p.rating
        for c in comments:
            posts_rating += c.rating
        for cp in comments_posts:
            posts_rating += cp.rating

        self.rating = posts_rating * 3 + comments_rating + comments_posts_rating
        self.save()

        print(posts_rating)
        print("----------")
        print(comments_rating)
        print("----------")
        print(comments_posts_rating)

        



class Category(models.Model):
    name = models.CharField(max_length=60,unique=True)
    subscribers = models.ManyToManyField(User, blank= True, related_name= 'categories')

    def __str__(self) :
        return self.name()

class Post(models.Model):
    post_author = models.ForeignKey(Author,on_delete= models.CASCADE)
    choice= models.CharField(max_length=2,choices=CHOISE,default=news)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category,through="PostCategory")
    title =  models.CharField(max_length=100)
    post_text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating  += 1
        self.save()

    def dislike(self):
        self.rating  -= 1
        self.save()

    def preview(self):
        return self.post_text[0:124]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse_lazy('post_detail', kwargs = {'pk':self.pk})

        


class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE)
    category = models.ForeignKey(Category,on_delete= models.CASCADE)

class Comment(models.Model):
    comm_post = models.ForeignKey(Post,on_delete= models.CASCADE)
    comm_user = models.ForeignKey(User,on_delete= models.CASCADE)
    comm_text = models.TextField()
    comm_dati_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating  += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user