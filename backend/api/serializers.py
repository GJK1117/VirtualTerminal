from rest_framework import serializers
from api.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields=['id', 'title', 'content', 'created_at', 'updated_at']