#Serializing Django Objects
# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data. Let’s start creating a serializer, in file apis/serializers.py

# import serializer from rest_framework
from rest_framework import serializers
 
# import model from models.py
from .models import SanareSomaModel
 
# Create a model serializer
class SanareSomaSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = SanareSomaModel
        fields = ('title', 'description')