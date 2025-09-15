from rest_framework import serializers
 
class EmailValidateSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.EmailField(),allow_empty=False)
    