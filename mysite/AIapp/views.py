from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib import messages
from .models import Item, User
from .serializers import ItemSerializer, UserSerializer
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .vault import get_secret
from .apps import data, summary


# Create your views here.

def index(request):
    return redirect('/login/')

def login_page(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(UserName=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        if not User.objects.filter(UserPassword=password).exists():
            # Display an error message if the password does not exist
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        
    #print(data)
    context = {'message': summary,'data': data}
    return render(request, 'data.html', context)
    
class ItemsView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@csrf_exempt
def UserAPI (request, id=0):
    if (request.method=='GET' and int(id) > 0):
        users=user.objects.filter(userId=id)
        user_serializer=UserSerializer(user, many=True)
        return JsonResponse(user_serializer.data,safe=False)
    elif request.method=='GET':   
        users = user.objects.all()
        users_serializer=UserSerializer(users,many=True)
        return JsonResponse(users_serializer.data,safe=False)
    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        users_serializer=UserSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Record Inserted Successfully",safe=False)
        return JsonResponse("Oops...something went wrong.",safe=False)
    elif request.method=='PUT':
        user_data=JSONParser().parse(request)
        user=user.objects.get(userId=user_data['userId'])
        users_serializer=UserSerializer(user,data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Record Updated Successfully",safe=False)
        return JsonResponse("There is some error updating the record", safe=False)
    elif request.method=='DELETE':
        user=user.objects.get(userId=id)
        user.delete()
        return JsonResponse("Record Deleted Successfully",safe=False)
    