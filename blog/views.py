import http

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import APIException
from storages.backends.dropbox import DropboxStorage
from dropbox.exceptions import ApiError
from django.utils._os import safe_join


class ModifiedDropboxStorage(DropboxStorage):

    def url(self, name):
        # Get or create a shared link for the file to avoid temporary URL expiration
        if name == "/":
            name = ""
        full_path = safe_join(self.root_path, name).replace("\\", "/")
        shared_link_metadata = self.client.sharing_create_shared_link_with_settings(full_path)
        url = shared_link_metadata.url.replace('dl=0', 'dl=1')
        return url


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' or request.method == 'PATCH' and request.FILES.get('file'):
        uploaded_file = request.FILES['upload']

        storage = ModifiedDropboxStorage()
        filename = storage.save(f'images/{uploaded_file.name}', uploaded_file)

        try:
            dbx = storage.client
        except ApiError as e:
            return APIException(detail='Failed to connect to cloud', code=http.HTTPStatus.INTERNAL_SERVER_ERROR)
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
