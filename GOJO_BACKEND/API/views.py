
from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser, JSONParser
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserView(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serialized = UserSerializer(user)
            return Response(serialized.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serialized = UserSerializer(instance=user, data=request.data)
            if serialized.is_valid():
                serialized.save()

                return Response(serialized.data)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serialized = UserSerializer(instance=user, data=request.data)
            if serialized.is_valid():
                serialized.save()

                return Response(serialized.data)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ListUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user != None:
            serialized = UserSerializer(instance=user)
            login(request, user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):
    def post(self, request):
        try:
            user = request.user
            logout(request, user)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PostsView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        print(request.user)
        posts = Post.objects.all()
        serialized = PostSerializer(posts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serialized = PostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serialized = PostSerializer(post)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serialized = PostSerializer(instance=post, data=request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serialized = PostSerializer(instance=post, data=request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChatsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print("got in and the user is ", request.user)

        try:
            user = User.objects.get(id=request.user.id)
            print(f"user is {user}")
            chats = Chat.objects.filter(Q(owner1=user) | Q(owner2=user))
            print(chats)
            serialized = ChatSerializer(chats, many=True)
            print(f"serialized is {serialized.data}")
            return Response(serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        data = request.data
        serialized = ChatSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            chat = Chat.objects.get(id=pk)
            serialized = ChatSerializer(chat)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            chat = Chat.objects.get(id=pk)
            chat.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MessagesView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            chat = Chat.objects.get(id=pk)
            if chat.owner1.id != request.user.id and chat.owner2.id != request.user.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            messages = Message.objects.filter(chat=chat)
            serialized = MessageSerializer(messages, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        data = request.data
        try:
            chat = Chat.objects.get(id=pk)
            if chat.owner1.id != request.user.id and chat.owner2.id != request.user.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serialized = MessageSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                chat.last_message = serialized.text
                chat.save()
                return Response(serialized.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class MessageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, chat_pk, pk):
#         try:

#             message = Message.objects.get(id=pk)
#             serialized = MessageSerializer(message)
#             return Response(serialized.data, status=status.HTTP_200_OK)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         try:
#             message = Message.objects.get(id=pk)
#             serialized = MessageSerializer(instance=message, data=request.data)
#             if serialized.is_valid():
#                 serialized.save()
#                 return Response(serialized.data, status=status.HTTP_200_OK)
#             return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         try:
#             message = Message.objects.get(id=pk)
#             serialized = MessageSerializer(instance=message, data=request.data)
#             if serialized.is_valid():
#                 serialized.save()
#                 return Response(serialized.data, status=status.HTTP_200_OK)
#             return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             message = Message.objects.get(id=pk)
#             message.delete()
#             return Response(status=status.HTTP_200_OK)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
