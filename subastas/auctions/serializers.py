# auctions/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Operation, Bid

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email
        )
        return user
    
