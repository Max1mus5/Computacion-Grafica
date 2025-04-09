import os
import base64
import json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .Filter_Lib.Filters import ImageFilters

def index(request):
    """Vista principal que muestra la página de carga de imágenes."""
    return render(request, 'viewer/home.html')

@csrf_exempt
def process_image(request):
    """Vista para procesar la imagen y aplicar filtros."""
    if request.method == 'POST':
        # Obtener imagen en base64 del formulario
        image_data = request.POST.get('image_data')
        
        if not image_data:
            return JsonResponse({'error': 'No image data provided'}, status=400)
        
        try:
            # Decodificar la imagen en base64
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            
            # Convertir a imagen PIL
            img_data = base64.b64decode(imgstr)
            img = Image.open(BytesIO(img_data))
            
            # Convertir a array numpy para procesamiento
            img_array = np.array(img)
            
            # Procesar la imagen según los filtros seleccionados
            filter_type = request.POST.get('filter_type', '')
            
            # Aplicar filtro según el tipo solicitado
            if filter_type == 'brightness':
                factor = float(request.POST.get('brightness_factor', 1.0))
                result = ImageFilters.adjust_brightness(img_array, factor)
            elif filter_type == 'contrast':
                factor = float(request.POST.get('contrast_factor', 1.0))
                result = ImageFilters.adjust_contrast(img_array, factor)
            elif filter_type == 'rotate':
                angle = float(request.POST.get('rotation_angle', 0))
                result = ImageFilters.rotate_image(img_array, angle)
            elif filter_type == 'highlight':
                mode = request.POST.get('highlight_mode', 'light')
                result = ImageFilters.highlight_zones(img_array, mode)
            elif filter_type == 'rgb':
                red = request.POST.get('red', 'true') == 'true'
                green = request.POST.get('green', 'true') == 'true'
                blue = request.POST.get('blue', 'true') == 'true'
                result = ImageFilters.apply_rgb_filter(img_array, red, green, blue)
            elif filter_type == 'cmy':
                cyan = request.POST.get('cyan', 'true') == 'true'
                magenta = request.POST.get('magenta', 'true') == 'true'
                yellow = request.POST.get('yellow', 'true') == 'true'
                result = ImageFilters.apply_cmy_filter(img_array, cyan, magenta, yellow)
            elif filter_type == 'negative':
                result = ImageFilters.negative_image(img_array)
            elif filter_type == 'zoom':
                x = int(request.POST.get('zoom_x', img_array.shape[1] // 2))
                y = int(request.POST.get('zoom_y', img_array.shape[0] // 2))
                scale = float(request.POST.get('zoom_scale', 2.0))
                result = ImageFilters.zoom_image(img_array, x, y, scale)
            elif filter_type == 'binary':
                threshold = int(request.POST.get('threshold', 128))
                result = ImageFilters.binarize_image(img_array, threshold)
            elif filter_type == 'merge':
                # Si hay una segunda imagen para fusionar
                second_image_data = request.POST.get('second_image_data')
                if second_image_data:
                    _, imgstr2 = second_image_data.split(';base64,')
                    img_data2 = base64.b64decode(imgstr2)
                    img2 = Image.open(BytesIO(img_data2))
                    img_array2 = np.array(img2)
                    
                    # Determinar el tipo de fusión
                    merge_type = request.POST.get('merge_type', 'alpha')
                    
                    if merge_type == 'watermark':
                        # Usar el método de marca de agua
                        result = ImageFilters.watermark_merge_images(img_array, img_array2)
                    else:
                        # Usar el método de fusión con transparencia
                        alpha = float(request.POST.get('alpha', 0.5))
                        result = ImageFilters.merge_images(img_array, img_array2, alpha)
                else:
                    result = img_array
            else:
                # Si no se especifica filtro, devolver la imagen original
                result = img_array
            
            # Convertir el resultado a imagen PIL
            result_img = Image.fromarray(result)
            
            # Convertir a base64 para devolver al cliente
            buffered = BytesIO()
            result_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Devolver la imagen procesada y datos adicionales
            return JsonResponse({
                'processed_image': f'data:image/png;base64,{img_str}',
                'filter_applied': filter_type
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def generate_histogram(request):
    """Vista para generar el histograma de la imagen."""
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        
        if not image_data:
            return JsonResponse({'error': 'No image data provided'}, status=400)
        
        try:
            # Decodificar la imagen en base64
            format, imgstr = image_data.split(';base64,')
            img_data = base64.b64decode(imgstr)
            img = Image.open(BytesIO(img_data))
            
            # Convertir a array numpy
            img_array = np.array(img)
            
            # Generar histograma
            fig = ImageFilters.generate_histogram(img_array)
            
            # Convertir figura a imagen
            buf = BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            plt.close(fig)
            buf.seek(0)
            
            # Codificar en base64
            img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # Calcular datos del histograma para la visualización
            hist_data = {
                'red': [],
                'green': [],
                'blue': [],
                'luminance': []
            }
            
            # Calcular histogramas
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                # Calcular luminancia
                luminance = np.dot(img_array[..., :3], [0.2989, 0.5870, 0.1140])
                hist_data['luminance'] = np.histogram(luminance, bins=256, range=(0, 256))[0].tolist()
                
                # Calcular histograma para cada canal
                hist_data['red'] = np.histogram(img_array[..., 0], bins=256, range=(0, 256))[0].tolist()
                hist_data['green'] = np.histogram(img_array[..., 1], bins=256, range=(0, 256))[0].tolist()
                hist_data['blue'] = np.histogram(img_array[..., 2], bins=256, range=(0, 256))[0].tolist()
            else:
                hist_data['luminance'] = np.histogram(img_array, bins=256, range=(0, 256))[0].tolist()
            
            return JsonResponse({
                'histogram_image': f'data:image/png;base64,{img_str}',
                'histogram_data': hist_data
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def editor(request):
    """Vista para la página del editor de imágenes."""
    return render(request, 'viewer/editor.html')