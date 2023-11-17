import json
import hashlib

from PIL import Image
from io import BytesIO
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from gym.models import Users, People, Roles
from gym.serializers import UserSerializer, PeopleSerializer, UserRoleSerializer

class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        people_data = json.loads(request.data.get('people', {}))

        existing_people = People.objects.filter(identification=people_data['identification']).first()
        if existing_people:
            return Response({'message': 'Ya existe una persona con esta identificación'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = json.loads(request.data.get('user', {}))
        image = request.FILES.get('image', None)

        if not user_data.get('username'):
            user_data['username'] = people_data['identification']

        if user_data.get('password'):
            password = user_data['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user_data['password'] = hashed_password
            search = 'admin'
        else:
            search = 'cliente'
        
        serializer = self.get_serializer(data=user_data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        people_data['userId'] = user.id
        people_serializer = PeopleSerializer(data=people_data)
        people_serializer.is_valid(raise_exception=True)
        
        people = people_serializer.save()

        if image:
            img = Image.open(image)
            img_bytes_io = BytesIO()
            img = img.convert('RGB')
            img.save(img_bytes_io, format='JPEG')
            people.image = img_bytes_io.getvalue()
            people.save()
        
        role, created = Roles.objects.get_or_create(name=search)
        user_roles_serializer = UserRoleSerializer(data={'userId': user.id, 'roleId': role.id})
        user_roles_serializer.is_valid(raise_exception=True)
        user_roles_serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Usuario creado', 'id': user.id}, status=status.HTTP_201_CREATED, headers=headers)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Users.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        user_data = json.loads(request.data.get('user', {}))
        people_data = json.loads(request.data.get('people', {}))
        image = request.FILES.get('image', None)

        del user_data['password']

        serializer = self.get_serializer(user, data=user_data, partial=True)
        serializer.is_valid(raise_exception=True)

        people_data = json.loads(request.data.get('people', {}))
        people = People.objects.filter(identification=people_data['identification']).first()
        people_data['userId'] = user.id

        people_serializer = PeopleSerializer(people, data=people_data, partial=True)
        people_serializer.is_valid(raise_exception=True)

        if image:
            img = Image.open(image)
            img_bytes_io = BytesIO()
            img = img.convert('RGB')
            img.save(img_bytes_io, format='JPEG')
            people.image = img_bytes_io.getvalue()
            people.save()
        
        return Response({'message': 'Usuario actualizado', 'id': user.id}, status=status.HTTP_200_OK)

class UserDeleteView(generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({'message': 'Usuario eliminado'}, status=status.HTTP_204_NO_CONTENT)