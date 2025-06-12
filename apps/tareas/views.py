from django.shortcuts import render
from .models import Tareas
from django.db.models import Q
from django.core.paginator import Paginator

def tareas(request):
    profile = request.user.profile_set.first()
    tareas_list = Tareas.objects.filter(profile=profile).order_by('nombre')

    # Búsqueda
    search_query = request.GET.get('filter', '')
    if search_query:
        tareas_list = tareas_list.filter(
            Q(nombre__icontains=search_query) 
        )
    
    # Paginación (fuera del if para que aplique siempre)
    paginator = Paginator(tareas_list, 3)
    page_number = request.GET.get('page')
    tareas = paginator.get_page(page_number)

    context = {
        'tareas': tareas,
        'search_query': search_query  # Opcional: para mantener el valor en el input
    }

    return render(request, 'tareas.html', context)