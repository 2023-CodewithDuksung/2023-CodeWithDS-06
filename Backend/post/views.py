from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post
from .forms import PostForm
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'

def single_post(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'post/single_post.html',
        {
            'post': post,
        }
    )

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'post/post_form.html', {'form': form})