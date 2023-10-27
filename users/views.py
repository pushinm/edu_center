from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer, MyUserLoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import MyUser
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .token_generator import email_verification_token
from django.core.mail import EmailMessage
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import get_user_model


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self._send_email_verification(user)
            return Response({
                "user": serializer.data,
                "success": "True",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _send_email_verification(self, user: MyUser):
        current_site = get_current_site(request=self.request)
        subject = 'Activate your profile'
        body = render_to_string(
            'emails/email_verification.html',
            {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            }
        )
        EmailMessage(to=[user.email], subject=subject, body=body).send()


class CustomAuthToken(ObtainAuthToken):
    serializer_class = MyUserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class Logout(APIView):
    def get(self, request, format=None):
        # Typically, the token is in the 'Authorization' header
        auth_header = request.headers.get('Authorization')
        if auth_header is not None:
            # Assuming token is prefixed with 'Token '
            token_string = auth_header.split(' ')[1]
        else:
            return Response({"detail": "Authorization header not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = Token.objects.get(key=token_string)
            token.delete()
            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


class ActivateView(View):
    def get_user_from_email_verification_token(self, token, uidb64):
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(f'UIDDDDDD: {uid}')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                get_user_model().DoesNotExist):
            return None

        if user is not None \
                and \
                email_verification_token.check_token(user, token):
            return user

        return None
        # def get_user_from_email_verification_token(self, token: str, uidb64):
        #     try:
        #         print('token:', token)
        #         uid = force_str(urlsafe_base64_decode(uidb64))
        #         print('UID:', uid)
        #         user = get_user_model().objects.get(pk=uid)
        #         print('1:', user)
        #     except (TypeError, ValueError, OverflowError,
        #             get_user_model().DoesNotExist):
        #         return None

        # if user is not None and email_verification_token.check_token(user, token):
        #     print('2', user)
        #     return user
        # else:
        #     print(3)
        #     return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64=uidb64, token=token)
        print(user)
        user.is_active = True
        user.save()
        return redirect('/')
