
from rest_framework import serializers
from users.models import User

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 
                'username', 
                'email', 
                'first_name', 
                'last_name', 
                'gender')
        read_only_fields = ('email', 'pk')

