from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post 
from .forms import PostForm 
from django.shortcuts import render
from django.http import JsonResponse
import logging

# Create your views here.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    csv_import = post.csv_file
    filtered_data = None
    name = None
    if request.method == 'POST':
        name = request.POST.get('name', '')
        if post.csv_file:
            filtered_data = post.filter_csv_data_by_name(name)
    
    return render(request, 'blog/post_detail.html', {'post': post, 'csv_import': csv_import, 'filtered_data': filtered_data, 'name': name})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    col4_values = set()
    for post in posts:
        if post.csv_file:
            csv_data = post.read_csv_data()
            for row in csv_data:
                if len(row) > 3:
                    col4_values.add(row[3])
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': col4_values})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def search_by_name(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        search_results = []
        posts = Post.objects.all()
        for post in posts:
            if post.csv_file:
                csv_data = post.filter_csv_data_by_name(name)
                for row in csv_data:
                    if len(row) > 1 and name.lower() in row[1].lower():
                        search_results.append(row)  # Ajouter la ligne correspondante aux résultats de recherche

        return render(request, 'blog/search_results.html', {'search_results': search_results})  # Renvoyer les résultats de la recherche en HTML
    return render(request, 'blog/search_results.html', {'search_results': []})




logger = logging.getLogger(__name__)

def calculate_averages(request):
    if request.method == 'GET':
        logger.debug("Calculating averages")
        categories = set()
        
        # Récupération des données des posts avec des fichiers CSV
        posts = Post.objects.filter(csv_file__isnull=False)
        for post in posts:
            csv_data = post.read_csv_data()
            for row in csv_data:
                # Vérification de la présence de la colonne de catégorie
                if len(row) > 3:
                    categories.add(row[3])  # Ajouter la catégorie à l'ensemble
        
        # Créer une liste à partir de l'ensemble pour pouvoir la retourner en JSON
        category_list = list(categories)
        logger.debug("Categories: %s", category_list)
        
        # Renvoyer les catégories en JSON
        return JsonResponse(category_list, safe=False)
    
    # Si la méthode de la requête n'est pas GET, renvoyer une réponse d'erreur
    return JsonResponse({'error': 'Méthode de requête invalide'}, status=400)











             




          
