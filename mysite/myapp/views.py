from rest_framework.views import APIView
from django.views.decorators.http import require_http_methods

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.settings import api_settings
from .models import *
from django.http import JsonResponse
import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        #users = student.objects.all()
        pass
        #return Response(data)

class userdata(object):
    def __int__(self):
        pass
    @csrf_exempt
    def get_token(self, request):
        if request.method.lower() != "post":
            json_data = {"Error": "This url only supports POST"}
            return JsonResponse(json_data)
        json_data = {}
        if "student" in request.path.lower():
            model = student
        elif "teacher" in request.path.lower():
            model = teacher
        payload = json.loads(request.body)
        data = model.objects.filter(username=payload["username"],
                                    password=payload["password"])
        if data:
            json_data["access_id"] = str(jwt.encode(payload, settings.SECRET_KEY))
            json_data["message"] = "Valid User"
        else:
            json_data["Error"] = "Failed to authenticate user or user doesnot exist"
        return JsonResponse(json_data)

    def authenticate(self, request):
        try:
            data_key = request.headers['Authorization']
            data_key = data_key.split(" ")[1]
        except Exception:
            json_data = {"Error": "Please provide access token"}
            return JsonResponse(json_data)
        try:
            json_data = jwt.decode(data_key, settings.SECRET_KEY)
        except jwt.DecodeError as e:
            json_data = {"Error": "Failed to authenticate with error {0}".format(e)}
        except jwt.ExpiredSignatureError:
            json_data = {"Error": "Signature has expired, please generate new one"}
        return json_data

    def get_model(self, request):
        if "student" in request.path.lower():
            model = student
        elif "teacher" in request.path.lower():
            model = teacher
        return model

    def get_data(self, request):
        model = self.get_model(request)
        payload = self.authenticate(request)
        if payload.get("Error"):
            return JsonResponse(payload)
        data = model.objects.filter(username=payload["username"],
                                    password=payload["password"]).values()
        if data:
            json_data = data[0]
            if json_data.get("teacher_id"):
                json_data["teacher_id"] = teacher.objects.filter(
                    id=json_data["teacher_id"]).values()[0]
        else:
            json_data = {"Error": "User doesnt exist"}
        return JsonResponse(json_data)

    @csrf_exempt
    def patch_data(self, request):
        if request.method.lower() != "patch":
            json_data = {"Error": "This url only supports PATCH"}
            return JsonResponse(json_data)
        model = self.get_model(request)
        payload = self.authenticate(request)
        id_data = model.objects.filter(username=payload["username"],
                                    password=payload["password"]).values('id')
        update_data = json.loads(request.body)
        if payload.get("Error"):
            return JsonResponse(payload)
        model.objects.filter(id=id_data[0]['id']).update(**update_data)
        json_data = {"Message": "Updated successfully"}
        return JsonResponse(json_data)

    def view_data(self, request):
        fin_data = {}
        if request.method.lower() != "get":
            json_data = {"Error": "This url only supports GET"}
            return JsonResponse(json_data)
        data = student.objects.all()
        for item in data.values():
            fin_data[item["id"]] = item
            if item.get("teacher_id"):
                fin_data[item["id"]]["teacher_id"] = teacher.objects.filter(
                    id=item["teacher_id"]).values()[0]
        return render(request, template_name="myapp/test.html", context={'final': fin_data})
