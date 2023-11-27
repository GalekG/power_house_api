# Generated by Django 4.2.6 on 2023-11-27 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=25)),
                ('muscleGroup', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('image', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Exercises',
            },
        ),
        migrations.CreateModel(
            name='Machines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('muscleGroup', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=1)),
                ('image', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Machines',
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('identification', models.CharField(max_length=25, unique=True)),
                ('names', models.CharField(max_length=50)),
                ('lastnames', models.CharField(max_length=50)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('mobile', models.CharField(max_length=11, null=True)),
                ('weight', models.IntegerField()),
                ('height', models.IntegerField()),
                ('bloodType', models.CharField(max_length=5, null=True)),
                ('gender', models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro')], max_length=15)),
                ('image', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'People',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Routines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(null=True)),
                ('difficulty', models.CharField(default='Principiante', max_length=25)),
                ('goal', models.CharField(max_length=25)),
                ('muscleGroup', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'Routines',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('roleId', models.ForeignKey(db_column='roleId', on_delete=django.db.models.deletion.CASCADE, to='gym.roles')),
                ('userId', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.CASCADE, to='gym.users')),
            ],
            options={
                'db_table': 'UserRoles',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('value', models.FloatField()),
                ('peopleId', models.ForeignKey(db_column='peopleId', on_delete=django.db.models.deletion.CASCADE, to='gym.people')),
            ],
            options={
                'db_table': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='RoutinesExercises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('exerciseId', models.ForeignKey(db_column='exerciceId', on_delete=django.db.models.deletion.CASCADE, to='gym.exercises')),
                ('routineId', models.ForeignKey(db_column='routineId', on_delete=django.db.models.deletion.CASCADE, to='gym.routines')),
            ],
            options={
                'db_table': 'RoutinesExercises',
            },
        ),
        migrations.CreateModel(
            name='RoutineSchedules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('dayOfWeek', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=15)),
                ('peopleId', models.ForeignKey(db_column='peopleId', on_delete=django.db.models.deletion.CASCADE, to='gym.people')),
                ('routineId', models.ForeignKey(db_column='routineId', on_delete=django.db.models.deletion.CASCADE, to='gym.routines')),
            ],
            options={
                'db_table': 'RoutineSchedules',
            },
        ),
        migrations.AddField(
            model_name='people',
            name='userId',
            field=models.ForeignKey(blank=True, db_column='userId', null=True, on_delete=django.db.models.deletion.CASCADE, to='gym.users'),
        ),
        migrations.CreateModel(
            name='ExerciseMachines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('exerciseId', models.ForeignKey(db_column='exerciceId', on_delete=django.db.models.deletion.CASCADE, to='gym.exercises')),
                ('machineId', models.ForeignKey(db_column='machineId', on_delete=django.db.models.deletion.CASCADE, to='gym.machines')),
            ],
            options={
                'db_table': 'ExerciseMachines',
            },
        ),
    ]
