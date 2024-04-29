import os
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from movies_app.models import *
import sweetify
from .models import Movies, Category

def search(request):
    if request.method=='POST':
        s=request.POST['search']
        print(s)
        try:
           film=Movies.objects.get(m_title=s)
           return render(request,'search.html',{'film':film})
           
        except:
            msg="Movie not Found"
            sweetify.error(request,"Movie not Found. Try again.")
            return redirect('home')
            return render(request,'Login.html',{'message':msg})
         
def movie_details(request):
    if request.method == 'POST':
        d = request.POST.get('movie_details')
        print(d)
        try:
            film = Movies.objects.get(m_title=d)
            return render(request,'movie_details.html', {'film': film})
        except Movies.DoesNotExist:
            msg = "Movie not Found"
            sweetify.error(request,"Movie not Found. Try again.")
            return render(request, 'home.html', {'message': msg})
    else:
        # Handle GET request, maybe redirect to the home page or render an error page
        return redirect('home')  
    
def show_movies_by_category(request, category_id):
    # Retrieve the category object using the id
    category = get_object_or_404(Category, id=category_id)
    
    # Filter movies based on the selected category
    movies = Movies.objects.filter(m_cat=category)
    
    context = {
        'category': category,
        'movies': movies
    }
    return render(request, 'movies_by_category.html', context)

# def show_movies_by_category(request, category):
#     # Filter movies based on the selected category
#     movies = Movies.objects.filter(m_cat=category)
#     context = {
#         'category': category,
#         'movies': movies
#     }
#     return render(request, 'movies_by_category.html', context)

def home(request):
    prd = Movies.objects.all()
    catgry = Category.objects.all()
    return render(request,'home.html',{'prd':prd,'catg':catgry})

def Eadmin(request):
    return render(request,"admin.html")

def Euser(request):
    usr = User.objects.get(username=u_name)
    user=Users.objects.get(e_user=usr)
    return render(request,'c_users.html',{'usr':user})

def loginpage(request):
    return render(request,'Login.html')

def signuppage(request):
    return render(request,'signup.html')

def add_movie(request):
    catg = Category.objects.all()
    return render(request,'admin/amovie.html',{'catg':catg})

def showmovie(request):  
    scatg = Category.objects.all()
    sprd = Movies.objects.all()
    return render(request,'admin/smovie.html',{'cat':scatg,'prod':sprd})

def edit_movie(request,od):
    ecatg = Category.objects.all()
    prd = Movies.objects.get(id=od)
    return render(request,'admin/emovie.html',{'ecatg':ecatg,'prod':prd})

def add_category(request):
    usr = Users.objects.all()
    return render(request,'admin/acategory.html')

def add_cat(request):
    if request.method == 'POST':
        pcatg = request.POST['pcatgr']
        catg = Category(c_category=pcatg)
        catg.save()
        # Retrieve all categories after adding a new one
        catg = Category.objects.all()
        return render(request, 'admin/acategory.html', {'catg': catg})
    

def show_category(request):
    catgry = Category.objects.all()
    return render(request,'admin/shocateg.html',{'catg':catgry})

def edit_category(request,od):
    catgry = Category.objects.get(id=od)
    return render(request,'admin/ecategory.html',{'catg':catgry})

def show_user(request): #admin.....
    usr = Users.objects.all()
    return render(request,'admin/showusers.html',{'user':usr})

def uprofile(request):
    usr = User.objects.get(username=u_name)
    user=Users.objects.get(e_user=usr)
    # data = User.objects.get(username=u_name) 'data':data,
    print(user)
    global data1
    data1= Users.objects.get(e_user=usr)
    print(data1)
    return render(request,'profile.html',{ 'data1':data1,'usr':user})   

def Login(request):
    if request.method == 'POST':
        global u_name
        u_name = request.POST['logname']
        pawd = request.POST['passw']
        log= auth.authenticate(username = u_name, password = pawd)
        if log is not None:
            if log.is_staff:
                auth.login(request,log)
                return redirect('Eadmin')
            else:
                auth.login(request,log)
                sweetify.success(request,'Login successful')
                return redirect('Euser')
        else:
            sweetify.error(request,"User name or password does not match. Try again.")
            return redirect('Login')


def Signup(request):
    if request.method == 'POST':
        Fname = request.POST['fname']
        Lname = request.POST['lname']
        usernam = request.POST['uname']
        e_mail = request.POST['E-mail']
        paswd = request.POST['pswd']
        cpaswd = request.POST['cpswd']
        
        if paswd != cpaswd:
            print("Passwords do not match! Please try again.")
            sweetify.error(request,"Passwords do not match! Please try again")
            return redirect('signuppage')  # Redirect to signup page

        if User.objects.filter(username=usernam).exists():
            print("This username already exists")
            sweetify.error(request,"User name already exist")
            return redirect('signuppage')  # Redirect to signup page

        user = User.objects.create_user(username=usernam, first_name=Fname,
                                         last_name=Lname, email=e_mail, password=paswd)
        user.save()

        # Create and save associated user data
        fuser = User.objects.get(username=usernam)
        custm = Users(e_fname=Fname, e_lname=Lname, e_email=e_mail, e_user=fuser)
        custm.save()
        sweetify.success(request,"Your account has been registered successfully.")
        return redirect('loginpage')  # Redirect to login page if signup is successful

    else:
        # Handle GET request for the signup page
        return render(request, 'signup.html')

def eprofile(request):
    if request.method=='POST':
        us = User.objects.get(username=u_name)
        us.first_name=request.POST['pfname']
        us.last_name=request.POST['plname']
        us.save()
        #cust = Users.objects.get(e_user=us)
        data1.e_fname = request.POST['pfname']
        data1.e_lname = request.POST['plname']
        data1.e_email = request.POST['e-mail']
        try:
            if len(request.FILES)!=0:
                try:
                    if len(data1.e_photo)>0:
                        os.remove(data1.e_photo.path)
                    data1.e_Photo = request.FILES['photo']
                except:
                    None
                data1.e_photo = request.FILES['photo']
        except:
            data1.e_photo = request.FILES['photo']
        data1.save()
        sweetify.success(request,"Data successfully Updated")
        return redirect('Euser')

def a_category(request):
    if request.method == 'POST':
        pcatg = request.POST['pcatgr']
        catg = Category(c_category= pcatg)
        catg.save()
        return redirect('add_category')

def e_category(request,od):
    if request.method == 'POST':
        catg = Category.objects.get(id=od)
        catg.c_category = request.POST['npcatgr']
        catg.save()
        return redirect('show_category')
    
@login_required(login_url='loginpage')
def cart(request):
    current_user = request.user
    movies_in_cart = Movies.objects.filter(added_by=current_user)
    return render(request, 'cart.html', {'cart_movies': movies_in_cart})

def a_movie(request):
    if request.method == 'POST':
        pname = request.POST['prname']
        pdes = request.POST['prdesc']
        dob = request.POST['dob']
        act_name = request.POST['act_name']
        youtube = request.POST['youtube']
        pimg = request.FILES['primg']
        catg = request.POST['adcatg']
        cat = Category.objects.get(id=catg)

        new_movie = Movies.objects.create(
            m_title=pname,
            m_desc=pdes,
            m_DOB=dob,
            m_act=act_name,
            m_youtube=youtube,
            m_img=pimg,
            m_cat=cat,
            added_by=request.user  # Associate the movie with the current user
        )
        new_movie.save()
        return redirect('cart')

@login_required(login_url='loginpage')
def delete_movie(request, movie_id):
    try:
        movie_to_delete = Movies.objects.get(id=movie_id)
        # Check if the movie belongs to the current user before deleting
        if movie_to_delete.added_by == request.user:
            movie_to_delete.delete()
        else:
            # Handle case where user is not authorized to delete the movie
            return HttpResponse("You are not authorized to delete this movie.")
    except Movies.DoesNotExist:
        # Handle case where movie does not exist
        return HttpResponse("Movie does not exist.")
    return redirect('cart')

    

def e_movie(request,od):
    if request.method == 'POST':
        prod = Movies.objects.get(id=od)
        prod.m_title = request.POST['nprname']
        prod.m_desc = request.POST['nprdesc']
        prod.m_DOB = request.POST['nprdob']
        prod.m_act = request.POST['npract']
        prod.m_youtube = request.POST['npryoutube']
        prod.m_img = request.FILES['nprimg'] 
        catg = request.POST['nadcatg']
        cat = Category.objects.get(id=catg)
        prod.m_cat = cat
        prod.save()
        return redirect('showmovie')
    


def feed(request):
    feds = Review.objects.all()
    return render(request,'feedback.html',{'feeds':feds})

def show_feed(request):
    sfeed=Review.objects.all()
    return render(request,'admin/showfeed.html',{'sfeed':sfeed})

def show_efeed(request):
    efeed = Review.objects.all()
    return render(request,'admin/showefeed.html',{'efeed':efeed})

def tfeed(request):
        if request.method == 'POST':
            r_name=request.POST['fname']
            r_dob=request.POST['dob']
            r_post=request.POST['post']
            r_rating=request.POST['rating']
            r_review=request.POST['review']
            addfeed=Review(re_name=r_name,re_DOB=r_dob,re_feed=r_post,re_rating=r_rating,re_post=r_review )
            addfeed.save()
            sweetify.success(request,"Review has beign send")
            return redirect('feed')   
        
def delete_feed(request,od):
    sfeed=Review.objects.get(id=od)
    sfeed.delete()
    sweetify.success(request,"Review  deleted",button='Ok',timer=5000)
    return redirect('show_feed')

def delete_movie(request,od):
    prod=Movies.objects.get(id=od) 
    prod.delete()
    return redirect('showmovie')

def add_cart(request,od):
    prdt = Movies.objects.get(id=od)
    usr = User.objects.get(username=u_name)
    cut = Users.objects.get(e_user=usr)
    cart = Movie_cart(user=usr,movie=prdt)
    cart.save()
    cut.cart=cart
    cut.save()
    return redirect('home')

def show_user(request): #admin.....
    usr = Users.objects.all()
    return render(request,'admin/showusers.html',{'user':usr})


def deletecust(request,od):
    cust = Users.objects.get(id=od)
    catm = cust.e_user.id
    usr = User.objects.get(id=catm)
    usr.delete()
    cust.delete()
    return redirect("show_user")

def deletecart_item(request):
    current_id =request.user.id
    usr=User.object.get(id=current_id)
    return redirect('cart')
    
    

def deletecart_item(request,od):
    cust = Users.objects.get(id=od)
    usr =User.objects.get(username=u_name)
    ctm = Users.objects.get(e_user=usr)
    cart = Movie_cart.objects.get(user=usr)
    cart.delete()
    usr.delete()
    cust.delete()
    return redirect("cart")


@login_required(login_url='Login')
def Logout(request):
    auth.logout(request)
    return redirect('home')