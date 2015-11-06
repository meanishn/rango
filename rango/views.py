from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rango.models import Category
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from datetime import datetime
import redis
import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def ajax_index(request):
    sessions=request.user.session_set.all()
    cat_list=Category.objects.all().filter(user=request.user).order_by('name')
    return render(request,'rango/ajax_index.html',{'cat_list':cat_list,'sessions':sessions})

def index(request):
    category_list=Category.objects.all().order_by('-name')
    context={'categories':category_list,
             'user':request.user
             }
    visits=request.session.get('visits')
    if not visits:
        visits=1
    reset_last_visit_time=False
    last_visit=request.session.get('last_visit')
    
    if last_visit:
        last_visit_time=datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        if (datetime.now()- last_visit_time).seconds > 3:
            visits=visits+1
            reset_last_visit_time=True
        #context['visits']=visits
        #response=render(request,'rango/index.html',context)
    else:
        reset_last_visit_time=True
        context['visits']=visits
        #response=render(request,'rango/index.html',context)
    if reset_last_visit_time:
        request.session['last_visit']=str(datetime.now())
        request.session['visits']=visits
    context['visits']=visits
    response=render(request,'rango/index.html',context)
    return response

def about(request):
    return render(request,'rango/about.html','')

def details(request,category_name_slug):
    
    category=get_object_or_404(Category,slug=category_name_slug)
    
    context={'category':category}
    return render(request,'rango/details.html',context)

@login_required
def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            cat=form.save(commit=False)
            cat.user=request.user
            cat.save()
            return index(request)
        else:
            print (form.errors)
    else:
        form=CategoryForm()
    return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request, category_name_slug):
    #category_name=category_name.replace("-"," ")
    try:
        cat=Category.objects.get(slug=category_name_slug)
        
    except Category.DoesNotExist:
        cat=None
        
    
    if request.method=='POST':
        form=PageForm(request.POST)
        if form.is_valid():
            if cat:
                
                page=form.save(commit=False)
                page.category=cat
                page.views=0
                page.save()
                    
                return details(request,category_name_slug)
        else:
            print(form.errors)
                   
    else:
            form=PageForm()
    
    return render(request,'rango/add_page.html',{'form':form,'category':cat})
            

def register(request):
    if request.session.test_cookie_worked():
        print("Test cookie worked")
        request.session.delete_test_cookie()
    registered=False
    
    if request.method=='POST':
        user_form=UserForm(request.POST)
        profile_form=UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user= user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile=profile_form.save(commit=False)
            profile.user=user
            
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            profile.save()
            
            registered=True
        else:
            print (user_form.errors, profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    
    return render(request,'rango/register.html',
        {'user_form':user_form,'profile_form':profile_form,'registered':registered}
                  )
            
@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/rango')

@csrf_exempt
def demo_cat(request):
    if request.method == "POST":
        cat_id=request.POST['c_id']
        cat=Category.objects.get(id=cat_id)
        return HttpResponse('%s %s'%(cat.name,cat_id))
    else:
        print('not get')
        return HttpResponse('not valid')
    


  
def encode():
    category_list=Category.objects.all().order_by('-name')
    for category in category_list:
        category.url=category.name.replace(" ","_")
    return category.url


#@receiver(post_save, sender=Category)
def post_save_category(sender, **kwargs):
    redis_client=redis.StrictRedis()
    
    category=kwargs['instance']
    user=category.user
    for session in user.session_set.all():
        print(session.session_key)
        redis_client.publish('category-%s'%session.session_key, json.dumps(dict(name=category.name)))
    

 

    



    

    
     
