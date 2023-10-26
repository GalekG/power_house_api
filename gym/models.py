from django.db import models
from power_house.models import BaseModel

class Genders(BaseModel):
    name = models.CharField(max_length=25)

    class Meta:
        db_table = 'Genders'

class Users(BaseModel):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255, null=True, blank=True)
    identification = models.CharField(max_length=25)
    names = models.CharField(max_length=50)
    lastnames = models.CharField(max_length=50)
    birthdate = models.DateField()
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    weight = models.IntegerField()
    height = models.IntegerField()
    bloodType = models.CharField(max_length=5, null=True)
    genderId = models.ForeignKey(Genders, on_delete=models.CASCADE, null=True, blank=True, db_column='genderId')

    class Meta:
        db_table = 'Users'

class Roles(BaseModel):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'Roles'

class UserRoles(BaseModel):
    userId = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False, db_column='userId')
    roleId = models.ForeignKey(Roles, on_delete=models.CASCADE, null=False, blank=False, db_column='roleId')

    class Meta:
        db_table = 'UserRoles'

class DaysOfWeek(BaseModel):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'DaysOfWeek'

class Exercises(BaseModel):
    name = models.CharField(max_length=25)
    muscleGroup = models.CharField(max_length=50)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'Exercises'

class Machines(BaseModel):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True)
    muscleGroup = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'Machines'

class ExerciseMachines(BaseModel):
    exerciceId = models.ForeignKey(Exercises, on_delete=models.CASCADE, null=False, blank=False, db_column='exerciceId')
    machineId = models.ForeignKey(Machines, on_delete=models.CASCADE, null=False, blank=False, db_column='machineId')

    class Meta:
        db_table = 'ExerciseMachines'

class Routines(BaseModel):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True)
    difficulty = models.CharField(max_length=25, default='Principiante')
    goal = models.CharField(max_length=25)

    class Meta:
        db_table = 'Routines'

class RoutineSchedules(BaseModel):
    userId = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False, db_column='userId')
    routineId = models.ForeignKey(Routines, on_delete=models.CASCADE, null=False, blank=False, db_column='routineId')
    dayOfWeekId = models.ForeignKey(DaysOfWeek, on_delete=models.CASCADE, null=False, blank=False, db_column='dayOfWeekId')

    class Meta:
        db_table = 'RoutineSchedules'

class RoutinesExercises(BaseModel):
    routineId = models.ForeignKey(Routines, on_delete=models.CASCADE, null=False, blank=False, db_column='routineId')
    exerciseId = models.ForeignKey(Exercises, on_delete=models.CASCADE, null=False, blank=False, db_column='exerciceId')

    class Meta:
        db_table = 'RoutinesExercises'

class Memberships(BaseModel):
    userId = models.ForeignKey(Users, on_delete=models.CASCADE, null=False, blank=False, db_column='userId')
    class Meta:
        db_table = 'Memberships'

class Transactions(BaseModel):
    membershipId = models.ForeignKey(Memberships, on_delete=models.CASCADE, null=False, blank=False, db_column='membershipId')
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    value = models.FloatField(null=True)

    class Meta:
        db_table = 'Transactions'


