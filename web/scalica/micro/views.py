from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Following, ReverseFollowing, Post, FollowingForm, PostForm, MyUserCreationForm

import grpc

import suggestions_pb2
import suggestions_pb2_grpc


# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      f = Following.objects.get(follower_id=request.user.id,
                                followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user = User.objects.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  try:
    my_post = Post.objects.filter(user=request.user).order_by('-pub_date')[0]
  except IndexError:
    my_post = None
  follows = [o.followee_id for o in Following.objects.filter(
    follower_id=request.user.id)]
  post_list = Post.objects.filter(
      user_id__in=follows).order_by('-pub_date')[0:10]
  context = {
    'post_list': post_list,
    'my_post' : my_post,
    'post_form' : PostForm
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user = request.user
    new_post.pub_date = timezone.now()
    new_post.save()
    return home(request)
  else:
    form = PostForm
  return render(request, 'micro/post.html', {'form' : form})

def make_new_follow(request):
  follower = request.user
  followee = User.objects.get(id=int(request.POST['followee']))

  form = FollowingForm(request.POST)
  follow = form.save(commit=False)
  reverse_follow = ReverseFollowing()

  follow.follower = follower
  reverse_follow.follower = follower
  reverse_follow.followee = followee

  date = timezone.now()
  follow.follow_date = date
  reverse_follow.follow_date = date

  follow.id = (int(follower.id) << 13) + Following.objects.count()
  reverse_follow.id = (int(followee.id) << 17) + ReverseFollowing.objects.count()

  follow.save()
  reverse_follow.save()

def get_following_suggestions(user_id):
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = suggestions_pb2_grpc.SuggestionsStub(channel)
    request = suggestions_pb2.SuggestionsRequest()
    request.user_id = user_id
    response = stub.Suggest(request)
  return response.suggestions

@login_required
def follow(request):
  if request.method == 'POST':
    make_new_follow(request)
    return home(request)
  else:
    form = FollowingForm
  return render(request, 'micro/follow.html', {'form' : form})

@login_required
def suggest(request):
  if request.method == 'POST':
    make_new_follow(request)
    return home(request)
  else:
    user_id = request.user.id
    suggestions = get_following_suggestions(user_id=user_id)
    form = FollowingForm(id_list=suggestions) if len(suggestions) > 0 else None
  return render(request, 'micro/suggest.html', {'form' : form})
