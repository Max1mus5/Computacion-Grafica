from django.shortcuts import render

def paint_view(request):
    """
    Vista principal para la aplicacion de paint.
    """
    return render(request, 'paint/index.html')
