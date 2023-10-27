from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import MyUser
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = MyUser
        fields = ('email', 'full_name', 'password')
        extra_kwargs = {
            'full_name': {'required': True},
        }

    def create(self, validated_data):
        user = MyUser.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


# class MyUserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(label="Email")
#     password = serializers.CharField(
#         label="Password",
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#             user = authenticate(request=self.context.get('request'),
#                                 email=email, password=password)
#             if not user:
#                 msg = 'Unable to log in with provided credentials.'
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = 'Must include "email" and "password".'
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs


class MyUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            print(f'{user}')
            if user is None:
                raise serializers.ValidationError("Invalid email/password. Please try again.")

            if not user.is_active:
                raise serializers.ValidationError("User is deactivated.")

        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data
    # def validate(self, data):
    #     email = data.get("email")
    #     password = data.get("password")
    #
    #     if email and password:
    #         user = authenticate(request=self.context.get('request'), username=email, password=password)
    #
    #         if not user:
    #             msg = 'Unable to authenticate with provided credentials.'
    #             raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = 'Must include "email" and "password".'
    #         raise serializers.ValidationError(msg, code='authorization')
    #
    #     data['user'] = user
    #     return data
