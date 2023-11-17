import json

from rest_framework import generics, status
from rest_framework.response import Response

from gym.serializers import RoutineScheduleSerializer
from gym.models import RoutineSchedules

class RoutineSchedulesListView(generics.ListAPIView):
    queryset = RoutineSchedules.objects.all()
    serializer_class = RoutineScheduleSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoutineSchedulesByPeopleIdView(generics.ListAPIView):
    serializer_class = RoutineScheduleSerializer
    
    def get_queryset(self):
        people_id = self.kwargs['people_id']
        return RoutineSchedules.objects.filter(peopleId=people_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoutineScheduleDetailView(generics.RetrieveAPIView):
    queryset = RoutineSchedules.objects.all()
    serializer_class = RoutineScheduleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RoutineScheduleCreateView(generics.CreateAPIView):
    serializer_class = RoutineScheduleSerializer

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        routineSchedule = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Horario de rutina creado', 'id': routineSchedule.id}, status=status.HTTP_201_CREATED, headers=headers)
    
class RoutineScheduleUpdateView(generics.UpdateAPIView):
    serializer_class = RoutineScheduleSerializer
    queryset = RoutineSchedules.objects.all()

    def update(self, request, *args, **kwargs):
        routineSchedule = self.get_object()

        serializer = self.get_serializer(routineSchedule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Horario de rutina actualizado', 'id': routineSchedule.id}, status=status.HTTP_200_OK)

class RoutineScheduleDeleteView(generics.DestroyAPIView):
    queryset = RoutineSchedules.objects.all()
    serializer_class = RoutineScheduleSerializer

    def destroy(self, request, *args, **kwargs):
        routineSchedule = self.get_object()
        routineSchedule.delete()
        return Response({'message': 'Horario de rutina eliminado'}, status=status.HTTP_204_NO_CONTENT)