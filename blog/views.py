from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.user.is_authenticated:
        file = request.FILES['upload']
        file_path = default_storage.save(f"uploads/{file.name}", file)
        file_url = default_storage.url(file_path)
        return JsonResponse({'url': file_url})

    return JsonResponse({'error': 'Authentication required or invalid request'}, status=400)
