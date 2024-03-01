from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post 
from .forms import PostForm 
from django.shortcuts import render


# Create your views here.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    csv_import = post.csv_file

    # Gestion de la recherche par nom
    filtered_data = None
    name = None
    if request.method == 'POST':
        name = request.POST.get('name', '')
        if post.csv_file:
            filtered_data = post.filter_csv_data_by_name(name)
    
    return render(request, 'blog/post_detail.html', {'post': post, 'csv_import': csv_import, 'filtered_data': filtered_data, 'name': name})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def search_by_name(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        # Recherche par nom dans tous les posts
        posts = Post.objects.filter(csv_file__icontains=name)
        return render(request, 'search_results.html', {'posts': posts, 'name': name})
    return render(request, 'search_form.html')