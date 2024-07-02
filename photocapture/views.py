# photocapture/views.py

from django.shortcuts import render, redirect
from .forms import PhotoForm
from .models import Photo
from django.core.files.base import ContentFile

# photocapture/views.py
import base64
from django.shortcuts import render, redirect
from .forms import PhotoForm
import datetime

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        print(f"{form.is_valid()=}")
        # if form.is_valid():
            # If image was uploaded through traditional file input
        if 'image' in request.FILES:
            form.save()
        else:
            # If image was captured via webcam (base64 encoded)
            data_url = request.POST.get('image', '')
            format, imgstr = data_url.split(';base64,')
            ext = format.split('/')[-1]
            img_data = ContentFile(base64.b64decode(imgstr), name=f'photo.{ext}')
            photo = Photo(image=img_data, uploaded_at=datetime.datetime.now())
            photo.save()
            print(f"Phoro is saved")
        return redirect('photo_list')  # Redirect to photo list page
        # else:
        #     print(form.errors)
    else:
        form = PhotoForm()
    return render(request, 'photocapture/photo_upload.html', {'form': form})


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photocapture/photo_list.html', {'photos': photos})
