from asyncio.windows_events import NULL
from email import message
from django import apps, forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
import os
from .forms import UploadFileForm
from PIL import Image
import pytesseract
import re
import speech_recognition as sr 
import moviepy.editor as mp
from django.conf import settings
from django.core.files.storage import FileSystemStorage



def index(request):
    return render(request,'index.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f=request.FILES['filename']
            str_f=str(f)
            # print(request.POST['filetype'])
            if(request.POST['filetype'] == "0"):
                return render(request,"index.html", {'error':"Select a valid file type"})
            elif(request.POST['filetype']=="1"):
                error,text = img_to_text(f)
                return render(request,"index.html",{'text':text, 'error':error})
            elif(request.POST['filetype']=="2"):
                error,text = vdo_to_text(f,str_f)
                return render(request,"index.html",{'text':text, 'error':error})
            elif(request.POST['filetype']=="3"):
                error,text = ado_to_text(f,str_f)
                return render(request,"index.html",{'text':text, 'error':error})
        else:
            print("Something went wrong")
    else:
        form = UploadFileForm()
    
    return render(request, 'index.html',{"form":form})

def img_to_text(f):
    error = ""
    text = ""
    try:
        pytesseract.pytesseract.tesseract_cmd =  r'C:\Users\Vrushali\AppData\Local\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(Image.open(f), lang="eng")
        return error,text
    except:
        error = "This image file extension is not supported"
        return error,text

def vdo_to_text(f,str_f):
    error = ""
    result = ""
    try:
        fs = FileSystemStorage()
        filename = fs.save(str_f, f)
        uploaded_file_url = fs.url(filename)
        clip = mp.VideoFileClip(str_f)
        clip.audio.write_audiofile(r"Converted_audio.wav")
        audio = sr.AudioFile("Converted_audio.wav")
        r = sr.Recognizer()
        with audio as source:
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        os.remove("Converted_audio.wav")
        # os.remove(str(uploaded_file_url)[1:])
        return error,result
    except:
        error = "This video file extension is not supported"
        return error,result

def ado_to_text(f,str_f):
    error = ""
    result = ""
    try:
        fs = FileSystemStorage()
        filename = fs.save(str_f, f)
        uploaded_file_url = fs.url(filename)
        # clip = mp.VideoFileClip(str_f)
        # clip.audio.write_audiofile(r"Converted_audio.wav")
        audio = sr.AudioFile(str_f)
        r = sr.Recognizer()
        with audio as source:
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        # os.remove("Converted_audio.wav")
        # os.remove(str(uploaded_file_url)[1:])
        return error,result
    except:
        error = "This audio file extension is not supported"
        return error,result
