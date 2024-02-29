from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post , CSVImport
from .forms import PostForm , CSVImportForm
import pandas as pd
from django.http import JsonResponse

# Create your views here.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def csv_import_list(request):
    csv_imports = CSVImport.objects.all()
    return render(request, 'blog/csv_import_list.html', {'csv_imports': csv_imports})

def csv_import_detail(request, pk):
    csv_import = get_object_or_404(CSVImport, pk=pk)
    return render(request, 'blog/csv_import_detail.html', {'csv_import': csv_import})

def csv_import_new(request):
    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_import = form.save(commit=False)
            csv_import.user = request.user
            csv_import.save()
            return redirect('csv_import_detail', pk=csv_import.pk)
    else:
        form = CSVImportForm()
    return render(request, 'blog/csv_import_edit.html', {'form': form})
