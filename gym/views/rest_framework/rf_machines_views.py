import json

from PIL import Image
from io import BytesIO
from rest_framework import generics
from gym.models import Machines
from gym.serializers import MachineSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class MachinesListView(generics.ListAPIView):
    queryset = Machines.objects.all()
    serializer_class = MachineSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MachineDetailView(generics.RetrieveAPIView):
    queryset = Machines.objects.all()
    serializer_class = MachineSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MachineCreateView(generics.CreateAPIView):
    serializer_class = MachineSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        machine_data = json.loads(request.data.get('machine', {}))
        image = request.FILES.get('image', None)
        
        serializer = self.get_serializer(data=machine_data)
        serializer.is_valid(raise_exception=True)

        machine = serializer.save()

        if image:
            img = Image.open(image)
            img_bytes_io = BytesIO()
            img = img.convert('RGB')
            img.save(img_bytes_io, format='JPEG')
            machine.image = img_bytes_io.getvalue()
            machine.save()

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Máquina creada', 'id': machine.id}, status=status.HTTP_201_CREATED, headers=headers)
    
class MachineUpdateView(generics.UpdateAPIView):
    serializer_class = MachineSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Machines.objects.all()

    def update(self, request, *args, **kwargs):
        machine = self.get_object()

        machine_data = json.loads(request.data.get('machine', {}))
        image = request.FILES.get('image', None)

        serializer = self.get_serializer(machine, data=machine_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if image:
            img = Image.open(image)
            img_bytes_io = BytesIO()
            img = img.convert('RGB')
            img.save(img_bytes_io, format='JPEG')
            machine.image = img_bytes_io.getvalue()
            machine.save()

        return Response({'message': 'Máquina actualizada', 'id': machine.id}, status=status.HTTP_200_OK)

class MachineDeleteView(generics.DestroyAPIView):
    queryset = Machines.objects.all()
    serializer_class = MachineSerializer

    def destroy(self, request, *args, **kwargs):
        machine = self.get_object()
        machine.delete()
        return Response({'message': 'Máquina eliminada'}, status=status.HTTP_204_NO_CONTENT)