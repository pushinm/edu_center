# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import RegisterSerializer
#
#
# class RegisterAPIView(APIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({
#                 "user": serializer.data,
#                 "message": "User created successfully",
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
