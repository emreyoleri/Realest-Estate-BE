from rest_framework import serializers
from .models import Realtor
from listings.serializers import Base64ImageField

class RealtorSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = Realtor
        fields = "__all__"