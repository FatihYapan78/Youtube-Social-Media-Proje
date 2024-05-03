from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
@login_required(login_url='/login/')
@csrf_exempt
def index(request):
    posts = Post.objects.all().order_by("-date")
    girisli_profil = Profil.objects.get(user=request.user)
    comments = Comment.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        button = request.POST.get("button")
        # print(post_id)
        # print(button)
        if request.POST.get("postbtn") == "btnpost":
            image = request.FILES.get("image")
            description = request.POST.get("description")

            new_post = Post.objects.create(profil=girisli_profil, image=image, description=description)
            new_post.save()
            return redirect("index")
        elif button == "btnlike":
            if Post.objects.filter(id=post_id, likes=girisli_profil).exists():
                post.likes.remove(girisli_profil)
                post.save()
                return JsonResponse({"like_count": post.likes.count(), "liked_request_user":False})
            else:
                post.likes.add(girisli_profil)
                post.save()
                return JsonResponse({"like_count": post.likes.count(), "liked_request_user":True})
            
        elif button == "btnsave":
            if Post.objects.filter(id=post_id, post_save=girisli_profil).exists():
                post.post_save.remove(girisli_profil)
                post.save()
                return JsonResponse({"saved_request_user":False})
            else:
                post.post_save.add(girisli_profil)
                post.save()
                return JsonResponse({"saved_request_user":True})
        
        elif button == "btncomment":
            comment = request.POST.get("comment")
            new_comment = Comment.objects.create(profil=girisli_profil, post=post, comment=comment)
            new_comment.save()
            return JsonResponse({"comment_count":new_comment.post.comment_count, "comment_id":new_comment.id,"profil_foto":new_comment.profil.image.url,"comment":new_comment.comment,"profil":new_comment.profil.user.username})
        
        elif button == "commentdel":
            comment_id = request.POST.get("comment_id")
            comment = Comment.objects.get(id= comment_id)
            comment.delete()
            return JsonResponse({"comment_count":comment.post.comment_count})

        
    context={
        "posts":posts,
        "girisli_profil":girisli_profil,
        "comments":comments
    }
    return render(request, "index.html", context)

@login_required(login_url='/login/')
def profil(request, username):
    profil = Profil.objects.get(user__username=username)
    girisli_profil = Profil.objects.get(user= request.user)
    girisli_profil_takip = Takip.objects.filter(profil=girisli_profil)
    profil_takipler = Takip.objects.filter(profil=profil)
    profil_takipciler = Takipci.objects.filter(profil=profil)
    profil_gonderi_sayisi = Post.objects.filter(profil=profil).count()
    posts = Post.objects.filter(profil=girisli_profil)
    if request.method == "POST":
        if request.POST.get("profileditbtn") == "btnprofileedit":
            image = request.FILES.get("image")
            email = request.POST.get("email")
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            bio = request.POST.get("bio")
            password = request.POST.get("password")
            if image is None:
                image = profil.image

            if profil.user.check_password(password):
                profil.image = image
                profil.bio = bio
                profil.save()
                user = User.objects.get(username=profil.user.username)
                user.email = email
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect(f"/profil/{profil}")
            else:
                messages.warning(request, "Parola Hatalıdır. Lütfen Tekrar Deneyin.")
        else:
            if girisli_profil_takip:
                for takip in girisli_profil_takip:
                    if takip.takip_edilen == profil:
                        takip = Takip.objects.get(takip_edilen=profil)
                        takip.delete()
                        takipci = Takipci.objects.get(takip_eden=girisli_profil)
                        takipci.delete()
                        return redirect(f"/profil/{profil}")
                    else:
                        takip = Takip.objects.create(profil=girisli_profil,takip_edilen=profil)
                        takip.save()
                        takipci = Takipci.objects.create(profil=profil,takip_eden=girisli_profil)
                        takipci.save()
                        return redirect(f"/profil/{profil}")
            else:
                takip = Takip.objects.create(profil=girisli_profil,takip_edilen=profil)
                takip.save()
                takipci = Takipci.objects.create(profil=profil,takip_eden=girisli_profil)
                takipci.save()
                return redirect(f"/profil/{profil}")
    context={
        "profil":profil,
        "girisli_profil":girisli_profil,
        "girisli_profil_takip":girisli_profil_takip,
        "profil_takipler":profil_takipler,
        "profil_takipciler":profil_takipciler,
        "profil_gonderi_sayisi":profil_gonderi_sayisi,
        "posts":posts
    }
    return render(request, "profil.html", context)

@csrf_exempt
def Search(request):
    if "query" in request.GET and request.GET.get("query") != "":
        query = request.GET.get("query")
        profils = Profil.objects.filter(user__username__icontains = query)

    if request.method == "POST":
        query = request.POST.get("query")

        if not query:
            return JsonResponse({"profils":[]})

        profils = Profil.objects.filter(user__username__icontains = query)

        profiller = []
        for profil in profils:
            profiller.append({
                "profil":profil.user.username,
                "profil_foto":profil.image.url
            })
        return JsonResponse({"profiller":profiller})

    context={
        "profils":profils
    }
    return render(request, "search.html",context)

def Login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user is not None:
                    login(request, user)
                    return redirect("index")
                else:
                    messages.warning(request, "Böyle Bir Kullanıcı Bulunamadı. Lütfen Tekrar Deneyin.")
            else:
                messages.warning(request, "Parola Hatalıdır. Lütfen Tekrar Deneyin.")
        else:
            messages.warning(request, "Email Adresi Hatalıdır. Lütfen Tekrar Deneyin.")

    return render(request, "login.html")

def Register(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                user.save()
                login(request, user)
                return redirect(f"/profil/{user.username}")
            else:
                messages.warning(request, "Bu Email Adresi Başka Bir Kullanıcı Tarafından Kullanılıyor.")
        else:
            messages.warning(request, "Bu Kullanıcı Adı Başka Bir Kullanıcı Tarafından Kullanılıyor.")

    return render(request, "register.html")

def Logout(request):
    logout(request)
    return redirect("login")