
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import HttpResponse
import csv
# Create your views here.
from .forms import PostForm, SignUpForm
from .models import Post

#####################

# from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 

#####################

def post_list(request):
	if not request.user.is_authenticated():
		messages.error(request, "You are not logged in")
		return redirect("posts:login")

	queryset_list = Post.objects.filter(user = request.user )


	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(fullname__icontains=query)|
			Q(phone__icontains=query)|
			Q(address__icontains=query)|
			Q(nickname__icontains=query)
		).distinct()

	#queryset_list = Post.objects.all() #.order_by("-timestamp")
	paginator = Paginator(queryset_list, 4) #show how many blogs

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not integer deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		# if page out of range deliver last one
		queryset = paginator.page(paginator.num_pages)

	context = {
			"object_list": queryset,
			"title": "Contacts",
	}

	return render(request, "post_list.html", context)

##########################

def login_user(request):
	if request.method == 'POST':
		username = request.POST['Username']
		password = request.POST['Password']
		user = authenticate( username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('Login Successful!'))
			return redirect('posts:list')	
		else:
			messages.success(request, ('Error! Incorrect Username or Password'))
			return redirect('posts:login')
	else:
		return render(request, 'login.html', {})


###################

def logout_user(request):
	logout(request)
	messages.success(request, ('Successfully Logged Out!'))
	return render(request, 'edit.html', {})

##################

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request, user)
			messages.success(request, ('Registration Successful'))
			return redirect('posts:list')
	else:
		form = SignUpForm()

	context = {'form': form}

	return render(request, 'register.html',context)



def post_create(request):
	if not request.user.is_authenticated():
		messages.error(request, "You are not logged in")
		return redirect("posts:list")


	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()

		messages.success(request, "Succesfully Created")
		return redirect("posts:list")

	context = {
		"form" : form,
	}
	return render(request, "post_form.html", context)



def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	if not request.user.is_authenticated():
		messages.error(request, "You are not logged in")
		return redirect("posts:login")

	context = {
		"title": "Details",
		"instance": instance
	}
	return render(request, "post_detail.html", context)



# def post_drafts(request):
# 	if not request.user.is_authenticated():
# 		messages.error(request, "You are not logged in")
# 		return redirect("posts:list")

# 	queryset_list = Post.objects.filter(draft=True)

# 	query = request.GET.get("q")

# 	if query:
# 		queryset_list = queryset_list.filter(
# 			Q(title__icontains=query)|
# 			Q(content__icontains=query)
# 		).distinct()

# #	queryset_list = Post.objects.all() #.order_by("-timestamp")
# 	paginator = Paginator(queryset_list, 5) #show how many blogs

# 	page = request.GET.get('page')
# 	try:
# 		queryset = paginator.page(page)
# 	except PageNotAnInteger:
# 		#if page not integer deliver first page
# 		queryset = paginator.page(1)
# 	except EmptyPage:
# 		# if page out of range deliver last one
# 		queryset = paginator.page(paginator.num_pages)

# 	context = {
# 			"object_list": queryset,
# 			"title": "List",
# 	}

# 	return render(request, "edit.html", context)

# # copy paginator view def listing()

def post_update(request, id=None):
	if not request.user.is_authenticated():
		messages.error(request, "You do not have permission")
		return redirect("posts:list")

	instance = get_object_or_404(Post, id=id)

	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	context = {
		"title": "Update Contact",
		"instance": instance,
		"form": form,
	}

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		messages.success(request, "Update Succesfull")

		return redirect("posts:list")

	
	return render(request, "post_form.html", context)

def post_delete(request, id=None):
	if not request.user.is_authenticated():
		messages.error(request, "You are not logged in")
		return redirect("posts:list")
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Succesfully Deleted !")

	return redirect("posts:list")


########################

def contact_download(request):
	if not request.user.is_authenticated():
		messages.error(request, "You do not have permission")
		return redirect("posts:list")

	items = Post.objects.filter(user = request.user)

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="contact.csv"'

	writer = csv.writer(response, delimiter=',')
	writer.writerow(['fullname',  'nickname',  'email',  'phone',  'address'])

	for obj in items:
		writer.writerow([obj.fullname, obj.nickname, obj.email, obj.phone, obj.address])

	return response
