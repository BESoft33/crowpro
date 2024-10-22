from django.core.files.storage import get_storage_class
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Use DropboxStorage from django-storages
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' or request.method == 'PATCH' and request.FILES.get('upload'):
        uploaded_file = request.FILES['upload']
        # Get Dropbox storage backend
        storage = get_storage_class('storages.backends.dropbox.DropBoxStorage')()
        # Save the uploaded file to Dropbox
        filename = storage.save(f'images/{uploaded_file.name}', uploaded_file)
        file_url = storage.url(filename)

        return JsonResponse({
            'url': request.build_absolute_uri(file_url),
            'file_name': filename,
            'uploaded': True
        })

    return JsonResponse({
        'error': 'No file uploaded',
        'uploaded': False
    })
