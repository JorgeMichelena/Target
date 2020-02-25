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
    gender = serializers.CharField(
        max_length=1,
        default='N',
    )
    
    def custom_signup(self, request, user):
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['gender'])
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        if data['gender'] not in ['F', 'M', 'N', 'O', '']:
            raise serializers.ValidationError(("Invalid input. Use 'F' for female, 'M' for male, or 'O' for other."))
        return data


