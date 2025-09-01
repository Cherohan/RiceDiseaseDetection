from django.shortcuts import render
from django.http import HttpResponse
from .models import Onnx_clf
from tkinter.filedialog import askopenfilename
import tkinter as tk

# Create your views here.

def index(request):
    return HttpResponse("测试！！！！！！！！！")

def nest(request):
    return render(request, "HTML/main.html")
def service_fit(request):
    return render(request, "HTML/service_fit.html") # 注意修改main.html文件里的文件路径
def service_repair(request):
    return render(request, "HTML/service_repair.html")
def drug_manure(request):
    return render(request, "HTML/drug_manure.html")
def drug_pesticide(request):
    return render(request, "HTML/drug_pesticide.html")
def accessory(request):
    return render(request, "HTML/accessory.html")
def consult(request):
    return render(request, "HTML/consult.html")
def detection_picture(request):
    clf = Onnx_clf()
    tk.Tk().withdraw()  # 隐藏主窗口, 必须要用，否则会有一个小窗口
    source = askopenfilename(title="打开保存的图片或视频")
    clf.img_identify() # 接收HTML上传的图片信息 clf.img_identify(img = 前端接收的图片)
    return render(request, "HTML/detection/picture_front.html")
def detection_vedio(request):
    clf = Onnx_clf()
    tk.Tk().withdraw()  # 隐藏主窗口, 必须要用，否则会有一个小窗口
    source = askopenfilename(title="打开保存的图片或视频")
    clf.video_identify() # 接收HTML上传的视频文件 clf.vedio_identify(vedio = 前端接收的图片)
    return render(request, "HTML/detection/vedio_front.html")
def detection_camera(request):
    clf = Onnx_clf()
    tk.Tk().withdraw()  # 隐藏主窗口, 必须要用，否则会有一个小窗口
    # source = askopenfilename(title="打开保存的图片或视频")
    clf.video_identify(0) #  clf.img_identify(img = 前端接收的图片)
    return render(request, "HTML/detection/detection_camera.html")