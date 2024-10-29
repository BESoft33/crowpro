from django.core.files.storage import get_storage_class
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from storages.backends.dropbox import DropboxStorage
from dropbox.exceptions import ApiError
from django.utils._os import safe_join

class ModifiedDropboxStorage(DropboxStorage):
    
    def url(self, name):
        # Get or create a shared link for the file to avoid temporary URL expiration
        if name == "/":
            name = ""
        full_path = safe_join(self.root_path, name).replace("\\", "/")
        print(full_path)
        shared_link_metadata = self.client.sharing_create_shared_link_with_settings(full_path)
        url = shared_link_metadata.url.replace('dl=0','dl=1')
        print(shared_link_metadata.url, url)
        return url

        

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' or request.method == 'PATCH' and request.FILES.get('upload'):
        uploaded_file = request.FILES['upload']

        # storage = get_storage_class('storages.backends.dropbox.DropBoxStorage')()
        storage = ModifiedDropboxStorage()
        # Save the uploaded file to Dropbox
        filename = storage.save(f'images/{uploaded_file.name}', uploaded_file)
        

        try:
            dbx = storage.client
            # shared_link_metadata = dbx.sharing_create_shared_link_with_settings(filename)
            # file_url = shared_link_metadata.url.replace('?dl=0', '?dl=1') 
            # print(file_url)
        except ApiError as e:
            # return JsonResponse({
            #     'error': f'Error creating shared link: {str(e)}',
            #     'uploaded': False
            # })
            print(str(e))

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
