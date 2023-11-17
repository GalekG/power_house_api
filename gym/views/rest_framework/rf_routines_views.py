import json

from rest_framework import generics, status
from rest_framework.response import Response

from gym.serializers import RoutineSerializer
from gym.models import Routines, Exercises, RoutinesExercises

class RoutinesListView(generics.ListAPIView):
    serializer_class = RoutineSerializer
    queryset = Routines.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoutineDetailView(generics.RetrieveAPIView):
    queryset = Routines.objects.all()
    serializer_class = RoutineSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoutineCreateView(generics.CreateAPIView):
    serializer_class = RoutineSerializer

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        routine_data = data.get('routine', {})
        exercises = data.get('exercises', [])
        
        serializer = self.get_serializer(data=routine_data)
        serializer.is_valid(raise_exception=True)

        routine = serializer.save()

        for exercise_id in exercises:
            try:
                exercise = Exercises.objects.get(pk=exercise_id)
                RoutinesExercises.objects.get_or_create(exerciseId=exercise, routineId=routine)
            except Exercises.DoesNotExist:
                return Response({'message': f'Ejercicio con ID {exercise_id} no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Rutina creada', 'id': routine.id}, status=status.HTTP_201_CREATED, headers=headers)
    
class RoutineUpdateView(generics.UpdateAPIView):
    serializer_class = RoutineSerializer
    queryset = Routines.objects.all()

    def update(self, request, *args, **kwargs):
        routine = self.get_object()

        data = json.loads(request.body)
        routine_data = data.get('routine', {})
        exercises = data.get('exercises', [])

        serializer = self.get_serializer(routine, data=routine_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        RoutinesExercises.objects.filter(routineId=routine).delete()
        for exercise_id in exercises:
            try:
                exercise = Exercises.objects.get(pk=exercise_id)
                RoutinesExercises.objects.get_or_create(exerciseId=exercise, routineId=routine)
            except Exercises.DoesNotExist:
                return Response({'message': f'Ejercicio con ID {exercise_id} no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Rutina actualizada', 'id': routine.id}, status=status.HTTP_200_OK)

class DeleteRoutineView(generics.DestroyAPIView):
    queryset = Routines.objects.all()
    serializer_class = RoutineSerializer

    def destroy(self, request, *args, **kwargs):
        routine = self.get_object()
        routine.delete()
        return Response({'message': 'Rutina eliminada'}, status=status.HTTP_204_NO_CONTENT)