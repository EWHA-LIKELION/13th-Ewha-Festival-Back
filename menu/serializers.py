from rest_framework.serializers import ModelSerializer, SerializerMethodField
from booths.models import Menu

class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'thumbnail', 'name', 'price', 'is_sale']
