import json

from PIL import Image
from io import BytesIO
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from gym.models import Exercises, Machines, ExerciseMachines
from gym.serializers import ExerciseSerializer

class ExerciseListView(generics.ListAPIView):
    queryset = Exercises.objects.all()
    serializer_class = ExerciseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExerciseDetailView(generics.RetrieveAPIView):
    queryset = Exercises.objects.all()
    serializer_class = ExerciseSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExerciseCreateView(generics.CreateAPIView):
    serializer_class = ExerciseSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        exercise_data = json.loads(request.data.get('exercise', {}))
        machines_ids = json.loads(request.data.get('machines', []))
        image = request.FILES.get('image', None)
        
        serializer = self.get_serializer(data=exercise_data)
        serializer.is_valid(raise_exception=True)

        exercise = serializer.save()

        if image:
            img = Image.open(image)
            img_bytes_io = BytesIO()
            img = img.convert('RGB')
            img.save(img_bytes_io, format='JPEG')
            exercise.image = img_bytes_io.getvalue()
            exercise.save()

        for machine_id in machines_ids:
            try:
                machine = Machines.objects.get(pk=machine_id)
                ExerciseMachines.objects.get_or_create(exerciseId=exercise, machineId=machine)
            except Machines.DoesNotExist:
                return Response({'message': f'Máquina con ID {machine_id} no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Ejercicio creado', 'id': exercise.id}, status=status.HTTP_201_CREATED, headers=headers)
    
class ExerciseUpdateView(generics.UpdateAPIView):
    serializer_class = ExerciseSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Exercises.objects.all()

    def update(self, request, *args, **kwargs):
        exercise = self.get_object()

        exercise_data = json.loads(request.data.get('exercise', {}))
        machines_ids = json.loads(request.data.get('machines', []))
        image = request.FILES.get('image', None)

        serializer = self.get_serializer(exercise, data=exercise_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if image:
            img = Image.open(image)
            img_bytes_io = BytesIO()
            img = img.convert('RGB')
            img.save(img_bytes_io, format='JPEG')
            exercise.image = img_bytes_io.getvalue()
            exercise.save()

        ExerciseMachines.objects.filter(exerciseId=exercise).delete()
        for machine_id in machines_ids:
            try:
                machine = Machines.objects.get(pk=machine_id)
                ExerciseMachines.objects.get_or_create(exerciseId=exercise, machineId=machine)
            except Machines.DoesNotExist:
                return Response({'message': f'Máquina con ID {machine_id} no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Ejercicio actualizado', 'id': exercise.id}, status=status.HTTP_200_OK)

class ExerciseDeleteView(generics.DestroyAPIView):
    queryset = Exercises.objects.all()
    serializer_class = ExerciseSerializer

    def destroy(self, request, *args, **kwargs):
        exercise = self.get_object()
        exercise.delete()
        return Response({'message': 'Ejercicio eliminado'}, status=status.HTTP_204_NO_CONTENT)