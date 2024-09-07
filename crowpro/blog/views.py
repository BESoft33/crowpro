# views.py
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .storage import CustomStorage


# TODO: Add cloud storage service for images

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' or request.method == 'PATCH' and request.FILES.get('file'):
        uploaded_file = request.FILES['upload']
        storage = CustomStorage()
        # storage = FileSystemStorage()
        filename = storage.save(uploaded_file.name, uploaded_file)
        file_url = storage.url(filename)

        return JsonResponse({
            'url':  request.build_absolute_uri(file_url),
            'file_name': filename,
            'uploaded': True
        })

    return JsonResponse({
        'error': 'No file uploaded',
        'uploaded': False
    })
