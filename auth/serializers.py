# from rest_framework import serializers
# from django.contrib.auth.password_validation import validate_password
# from .models import MyUser
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = MyUser
#         fields = ('email', 'full_name', 'password', 'password2')
#         extra_kwargs = {
#             'full_name': {'required': True},
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = MyUser.objects.create(
#             email=validated_data['email'],
#             full_name=validated_data['full_name']
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user