from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from users.models import User
from targets.models import Topic, Target
from targets.validators import less_than_max_targets
from chat.models import Match


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'gender')
        read_only_fields = ['email']


class RegisterSerializer(RegisterSerializer):

    gender = serializers.ChoiceField(choices=User.Gender.choices,)

    def custom_signup(self, request, user):
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['gender'])


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['pk', 'name', 'picture']


class TargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = ['pk', 'title', 'location', 'radius', 'topic']

    def create(self, validated_data):
        less_than_max_targets(self.context['request'].user)
        return super(TargetSerializer, self).create(validated_data)


class MatchSerializer(serializers.ModelSerializer):
    target1 = TargetSerializer()
    target2 = TargetSerializer()

    class Meta:
        model = Match
        fields = ['pk', 'creation_date', 'target1', 'target2']
