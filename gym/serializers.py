import base64

from rest_framework import serializers
from datetime import timezone, datetime
from gym.models import Users, People, Exercises, Machines, ExerciseMachines, Transactions, Routines, RoutinesExercises, RoutineSchedules, UserRoles
from django.core.exceptions import FieldDoesNotExist

class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance, show_created_updated=False):
        representation = super().to_representation(instance)

        if not show_created_updated:
            for field_name in ['created', 'updated']:
                representation.pop(field_name, None)

        image_field_name = 'image'
        try:
            image_field = instance._meta.get_field(image_field_name)
        except FieldDoesNotExist:
            return representation

        if image_field:
            image_data = getattr(instance, image_field_name, None)
            if image_data is not None:
                representation['image'] = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"

        return representation

    class Meta:
        model = None
        fields = '__all__'

class TransactionSerializer(BaseSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

class PeopleSerializer(BaseSerializer):
    transactions = TransactionSerializer(source='peopleId', read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        transactions = Transactions.objects.filter(peopleId=instance).values()

        representation['paymentStatus'] = 'Pendiente'
    
        if transactions:
            currentDate = datetime.now(timezone.utc).date()
            for transaction in transactions:
                if transaction['endDate'] >= currentDate:
                    representation['paymentStatus'] = 'Pagado'

        return representation
    class Meta:
        model = People
        fields = '__all__'

class UserSerializer(BaseSerializer):
    people = PeopleSerializer(source='userId', read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        people = People.objects.filter(userId=instance).first()
        representation['people'] = PeopleSerializer(people, many=False).data if people else {}
        return representation

    class Meta:
        model = Users
        exclude = ('password',)

class MachineSerializer(BaseSerializer):  
    class Meta:
        model = Machines
        fields = '__all__'

class ExerciseSerializer(BaseSerializer):  
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        exercise_machines = ExerciseMachines.objects.filter(exerciseId=instance)
        machines = [exercise_machine.machineId for exercise_machine in exercise_machines]
        representation['machines'] = MachineSerializer(machines, many=True).data
        return representation

    class Meta:
        model = Exercises
        fields = '__all__'

class RoutineExerciseSerializer:
    class Meta:
        model = RoutinesExercises
        fields = '__all__'

class RoutineSerializer(BaseSerializer):
    def to_representation(self, instance):
        presentation = super().to_representation(instance)
        routine_exercises = RoutinesExercises.objects.filter(routineId=instance)
        exercises = [routine_exercise.exerciseId for routine_exercise in routine_exercises]
        presentation['exercises'] = ExerciseSerializer(exercises, many=True).data
        return presentation

    class Meta:
        model = Routines
        fields = '__all__'

class RoutineScheduleSerializer(BaseSerializer):
    class Meta:
        model = RoutineSchedules
        fields = '__all__'

class UserRoleSerializer(BaseSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'