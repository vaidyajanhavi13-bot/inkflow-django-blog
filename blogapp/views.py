from django.shortcuts import render ,redirect ,get_object_or_404
from django.views import View
from blogapp.models import Blogs, Comment
from django.db.models import Q, Count 
from blogapp.forms import Add_Blog_Form , Edit_Blog_Form
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return redirect("/list/")

class List_view(View):

    def get(self, request, *args, **kwargs):

        search = request.GET.get("search")
        category = request.GET.get("category")

        data = Blogs.objects.all()
        popular_posts = Blogs.objects.annotate(total_likes=Count("liked_by")).order_by("-total_likes")[:3]

        if search:
            data = data.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )

        if category:
            data = data.filter(category=category)

        return render(
            request,
            "blogapp/list.html",
            {
                "data": data,
                "popular_posts": popular_posts,
                "selected_category": category,
            }
        )
    

class Detail_view(View):
    def get(self , request , *args , **kwargs):
        data = Blogs.objects.get(id=kwargs['id'])
        comments = data.comments.all().order_by('-created_at')

        return render(request, "blogapp/detail.html" ,{"data" :data , "comments": comments})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")

        data = get_object_or_404(Blogs, id=kwargs["id"])
        text = request.POST.get("text")


        if text:
            Comment.objects.create(blog=data,user=request.user,text=text)
        return redirect(f"/detail/{data.id}/")
    
    
class Create_view(LoginRequiredMixin ,View):
    login_url = "/login/"
    def get(self , request):
        form = Add_Blog_Form()
        return render(request , "blogapp/create.html" ,{"form" : form})
    
    def post(self , request):
        form = Add_Blog_Form(request.POST , request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('/list/')
        
        return render(request , "blogapp/create.html" , {"form" : form})
        

class Edit_view(LoginRequiredMixin ,View):
    login_url = "/login/"
    def get(self  , request , *args , **kwargs):
        obj = get_object_or_404(Blogs, pk=kwargs['id'],user=request.user)
        form = Edit_Blog_Form(instance=obj)

        return render(request ,"blogapp/edit.html" ,{"form" :form})

    def post(self, request , *args , **kwargs):
        obj = get_object_or_404(Blogs,pk=kwargs['id'],user=request.user)
        form = Edit_Blog_Form(request.POST ,request.FILES , instance = obj)

        if form.is_valid():
            form.save()
            return redirect(f"/detail/{obj.id}/")
        
        return render(request ,"blogapp/edit.html" , {"form" : form})
    

class Delete_view(LoginRequiredMixin ,View):
    login_url = "/login/"
    def get(self , request , *args , **kwargs):
        obj = get_object_or_404(Blogs, pk=kwargs['id'], user=request.user)
        obj.delete()
        return redirect('/list/')
    

class DashboardView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):

        blogs = Blogs.objects.filter(user=request.user).order_by("-date")

        total_blogs = blogs.count()

        total_likes = 0
        for blog in blogs:
            total_likes += blog.liked_by.count()

        total_comments = Comment.objects.filter(
            blog__user=request.user
        ).count()

        context = {
            "blogs": blogs,
            "total_blogs": total_blogs,
            "total_likes": total_likes,
            "total_comments": total_comments,
        }

        return render(request, "blogapp/dashboard.html", context)


def like_blog(request, id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "login": True
        })

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    blog = get_object_or_404(Blogs, id=id)

    if request.user in blog.liked_by.all():
        blog.liked_by.remove(request.user)
        liked = False
    else:
        blog.liked_by.add(request.user)
        liked = True

    return JsonResponse({
        "likes": blog.likes_count,
        "liked": liked
    })


def update_comment(request, id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=id, user=request.user)

        text = request.POST.get("text")

        comment.text = text
        comment.save()

        return JsonResponse({
            "success": True,
            "text": comment.text
        })

    return JsonResponse({"success": False})


class DeleteCommentView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id, user=request.user)
        blog_id = comment.blog.id
        comment.delete()
        return redirect(f"/detail/{blog_id}/")


