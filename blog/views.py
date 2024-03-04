from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post 
from .forms import PostForm 
from django.shortcuts import render
from django.http import JsonResponse


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

def search_by_name(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        search_results = {}
        posts = Post.objects.all()
        for post in posts:
            if post.csv_file:
                csv_data = post.read_csv_data()
                for row in csv_data:
                    if len(row) > 1 and name.lower() in row[1].lower():
                        if post.title not in search_results:
                            search_results[post.title] = set()
                        search_results[post.title].add(tuple(row))               
        for title, rows_set in search_results.items():
            search_results[title] = list(rows_set)
        return render(request, 'blog/search_results.html', {'search_results': search_results, 'name': name})
    return render(request, 'search_form.html')

def calculate_averages(request):
    if request.method == 'POST':
        selected_category = request.POST.get('selected_col4_value')
        if selected_category:
            total_speed = 0
            count = 0
            
            # Récupération des données des posts avec des fichiers CSV
            posts = Post.objects.filter(csv_file__isnull=False)
            for post in posts:
                csv_data = post.read_csv_data()
                for row in csv_data:
                    # Vérification de la catégorie et calcul de la moyenne de vitesse
                    if len(row) > 10 and row[3] == selected_category:
                        try:
                            total_speed += float(row[10])
                            count += 1
                        except ValueError:
                            pass  # Ignorer les valeurs non numériques
            
            # Calcul de la moyenne de vitesse
            if count > 0:
                average_speed = total_speed / count
                # Créez le HTML à renvoyer
                html_response = f"<p>L'average speed pour la catégorie {selected_category} est {average_speed}</p>"
                # Renvoyez une réponse HTTP avec le HTML
                return HttpResponse(html_response)
        
        # Si aucune catégorie n'est sélectionnée ou si aucune donnée n'est trouvée, renvoyer une réponse d'erreur
        return HttpResponse('<p>Erreur : catégorie invalide ou pas de données trouvées.</p>', status=400)

    # Si la méthode de la requête n'est pas POST, renvoyer une réponse d'erreur
    return HttpResponse('<p>Erreur : méthode de requête invalide.</p>', status=400)

                    

# def calculate_averages(request):
#    col4_values = set()
#    posts = Post.objects.all()
#    for post in posts:
#        if post.csv_file:
#            csv_data = post.read_csv_data()
#            for row in csv_data:
#                if len(row) > 3:
#                    col4_values.add(row[3])
#    print("Col4 values:", col4_values)
#    return render(request, 'blog/base.html', {'categories': col4_values})










             




          
