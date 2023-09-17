from django.shortcuts import render, redirect
from .forms import ImageForm
from eminem.models import Eminem

# ROBOFLOW PART

from roboflow import Roboflow
rf = Roboflow(api_key="e0YuF7qldXDOH0Ekelgy")
project = rf.workspace().project("car_plates-9970o")
model = project.version(2).model


# CROP PART

import cv2

def crop(img, preds, imname=None):

    y = round(preds['predictions'][0]['y'])
    height = round(preds['predictions'][0]['height'])
    x = round(preds['predictions'][0]['x'])
    width = round(preds['predictions'][0]['width'])

    x1 = round(x - (width/2))
    y1 = round(y - (height/2))
    x2 = round(x + (width/2))
    y2 = round(y + (height/2))

    cropped_image = img[y1:y2, x1:x2]

    cv2.imwrite(f"images/{imname}_cropped.jpg",cropped_image)

    return None

# OCR PART

import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

# URLs PART

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():

            field1 = form.cleaned_data['image']
            isinstance_temp = Eminem(image=field1)
            isinstance_temp.save()

            image = cv2.imread(f"images/{field1.name}")

            preds = model.predict(image, confidence=40, overlap=30).json()

            crop(image, preds, imname=field1.name)

            result = reader.readtext(f"images/{field1.name}_cropped.jpg")

            s = ''
            for i in result:
                s += i[1].replace(' ', '')
                s += ' '

            field2 = s

            isinstance = Eminem(image=field1, name=field2)
            isinstance.save()

            return render(request, 'eminem/results.html', {'text': field2}) # replace with your success URL
    else:
        form = ImageForm()
    return render(request, 'eminem/report.html', {'form': form})

def index(request):
    return render(request, 'eminem/index.html')

def aboutUS(request):
    return render(request, 'eminem/aboutUS.html')

def result(request):
    return render(request, 'eminem/result.html')