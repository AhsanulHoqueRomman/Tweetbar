from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet,Profile
from .forms import TweetForm, UserRegistrationForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets': tweets})

def profile_view(request, username):
    profile_user = User.objects.get(username=username)
    tweets = Tweet.objects.filter(user=profile_user).order_by('-created_at')
    return render(request,'profile.html',{'profile_user': profile_user,'tweets': tweets})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile',username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request,'edit_profile.html',{'form': form})

# Search View
def search_tweet(request):
    query = request.GET.get('q')
    tweets = Tweet.objects.filter(text__icontains=query).order_by('-created_at')
    return render(request,'search.html',{'tweets': tweets,'query': query})


@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
        
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


