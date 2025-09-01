from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.nest, name="nest"),
    path("test/", views.index, name="index"),
    path("serviceFit/", views.service_fit, name="serviceFit"),
    path("serviceRepair/", views.service_repair, name="serviceRepair"),
    path("accessory/", views.accessory, name="accessory"),
    path("drug_manure/", views.drug_manure, name="drugManure"),
    path("drug_pesticide/", views.drug_pesticide, name="drugPesticide"),
    path("consult/", views.consult, name="consult"),
    path("detection_picture/", views.detection_picture, name="detection_picture"),
    path("detection_vedio/", views.detection_vedio, name="detection_vedio"),
    path("detection_camera/", views.detection_camera, name="detection_camera"),
]