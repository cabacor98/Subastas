# auctions/views.py
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Operation, Bid
from .serializers import OperationSerializer, BidSerializer, UserRegistrationSerializer
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from .models import UserProfile
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate


class RegisterUser(APIView):
    def get(self, request):
        print("get--------------------", request)
        return render(request, 'auctions/register.html')

    def post(self, request):
        print("request--", request)
        serializer = UserRegistrationSerializer(data=request.data)
        print("serializer--", serializer)
        if serializer.is_valid():
            print("entra-----")
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            role = request.data.get('role')
            UserProfile.objects.create(user=user, role=role)
            print("pasa----------")
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OperationListCreate(generics.ListCreateAPIView):
    serializer_class = OperationSerializer
    permission_classes = []  
    def get_queryset(self):
        return Operation.objects.filter(is_closed=False)

    def perform_create(self, serializer):
        serializer.save()


class OperationDetail(generics.RetrieveAPIView):
    queryset = Operation.objects.all() 
    serializer_class = OperationSerializer
    permission_classes = []  

    def get(self, request, *args, **kwargs):
        print("Token recibido:", request.headers.get('Authorization'))
        return super().get(request, *args, **kwargs)

class BidCreate(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        print("antes de---")
        
        if user is not None:
            response = super().post(request, *args, **kwargs)
            print("user--", user)
            token = Token.objects.get_or_create(user=user)
            role = user.userprofile.role if hasattr(user, 'userprofile') else None
            
            return Response({
            'token': response.data['token'],
            'role': role
        })
        
        return Response({'error': 'Invalid credentials'}, status=400)

def login_page(request):
    print("llega login--", request.body)
    return render(request, 'auctions/login.html')

def index(request):
    return render(request, 'auctions/index.html')

def operation_list(request):
    operations = Operation.objects.filter(is_closed=False)
    return render(request, 'auctions/operation_list.html', {'operations': operations})

def bid_list(request, operation_id):
    operation = Operation.objects.get(id=operation_id)
    bids = operation.bids.all()
    return render(request, 'auctions/bid_list.html', {'operation': operation, 'bids': bids})