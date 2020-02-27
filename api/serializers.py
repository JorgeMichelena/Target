from rest_auth.registration.serializers import RegisterSerializer
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
        
class RegisterSerializer(RegisterSerializer):
    MALE = ('M', 'Male')
    FEMALE = ('F', 'Female')
    OTHER = ('O', 'Other')
    NOT_SPECIFIED = ('N', 'Not Specified')
    GENDERS = (
        MALE,
        FEMALE,
        OTHER,
        NOT_SPECIFIED,
    )
    gender = serializers.ChoiceField(choices=GENDERS,)
    
    def custom_signup(self, request, user):
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['gender'])
    


