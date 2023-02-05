from rest_framework import serializers
from .models import Realtor

class RealtorSerializer(serializers.ModelField):
    class Meta:
        model = Realtor
        fields = "__all__"