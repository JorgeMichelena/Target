from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from users.models import User
from targets.models import Topic

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
        
class RegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=User.GENDERS,)
    
    def custom_signup(self, request, user):
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['gender'])
    
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name', 'picture']


