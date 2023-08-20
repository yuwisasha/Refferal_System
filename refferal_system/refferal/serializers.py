import re

from rest_framework import serializers
from rest_framework.serializers import ReturnDict

from .models import User, SMSCode
from .utils import send_sms_code


class EntryAuthSertializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)

    def create(self, validated_data) -> SMSCode:
        phone_number = validated_data.get("phone_number")
        code = send_sms_code(phone_number)
        return SMSCode.objects.create(code=code, phone_number=phone_number)

    def validate_phone_number(self, phone_number: str) -> str:
        phone_number_pattern = re.compile("^9\d{9}")  # noqa
        if not re.match(phone_number_pattern, phone_number):
            raise serializers.ValidationError("Invalid phone number")
        return phone_number


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)
    code = serializers.CharField(max_length=4)

    def validate_code(self, code: str) -> str:
        if len(code) != 4 or not code.isdigit():
            raise serializers.ValidationError("Invalid code")
        return code


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone_number",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    invite_refferal_token = serializers.CharField(max_length=6)
    invited = serializers.SerializerMethodField()

    def get_invited(self, obj: User) -> ReturnDict:
        invited = User.objects.filter(
            invite_refferal_token=obj.personal_refferal_token
        )
        serializer = UserListSerializer(invited, many=True)
        return serializer.data

    def update(self, instance: User, validated_data) -> User:
        if instance.personal_refferal_token != validated_data.get(
            "invite_refferal_token"
        ):
            instance.invite_refferal_token = validated_data.get(
                "invite_refferal_token", instance.invite_refferal_token
            )
            instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            "phone_number",
            "personal_refferal_token",
            "invite_refferal_token",
            "invited",
        ]
