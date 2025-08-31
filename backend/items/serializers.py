from rest_framework import serializers
from .models import Item
from users.serializers import UserSerializer


class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Item
        fields = ['id', 'owner', 'owner_id', 'title', 'category', 'tags', 'description', 
                 'condition', 'image_urls', 'cloudinary_public_ids', 'number_of_items', 'is_available']
        read_only_fields = ['id']

    def create(self, validated_data):
        if 'owner_id' in validated_data:
            validated_data['owner_id'] = validated_data.pop('owner_id')
        return super().create(validated_data)


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'category', 'tags', 'description', 'condition', 
                 'image_urls', 'cloudinary_public_ids', 'number_of_items', 'is_available']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ItemListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    # Get the first image for thumbnail
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'title', 'category', 'tags', 'condition', 'image_urls', 
                 'thumbnail_url', 'is_available', 'owner_name', 'number_of_items']
    
    def get_thumbnail_url(self, obj):
        """Return the first image URL for use as thumbnail"""
        if obj.image_urls:
            return obj.image_urls[0]
        return None


class ItemDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
