from rest_framework import serializers
from .models import Ticket, User


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('pk', 'user_id', 'activated', 'created_at', 'used_at')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'middle_name',
                  'passport', 'date_of_birth', 'phone')