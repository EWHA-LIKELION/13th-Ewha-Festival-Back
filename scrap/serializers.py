from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *


class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth_scrap
        fields = '__all__'