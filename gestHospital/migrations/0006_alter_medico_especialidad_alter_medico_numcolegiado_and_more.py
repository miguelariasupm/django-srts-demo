# Generated by Django 5.1.3 on 2024-11-23 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestHospital', '0005_paciente_lesion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='Especialidad',
            field=models.CharField(choices=[('trauma', 'Traumatology'), ('cirugia', 'Surgery'), ('cardiologia', 'Cardiology'), ('neorulogia', 'Neurology'), ('urologia', 'Urology'), ('oftalmologia', 'Ophthalmology')], max_length=15),
        ),
        migrations.AlterField(
            model_name='medico',
            name='NumColegiado',
            field=models.CharField(help_text='License Number', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Documentacion',
            field=models.CharField(choices=[('Nº S.S.', 'Social Security Number'), ('NIF/NIE', 'NIF/NIE')], default='Nº S.S.', max_length=25),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Lesion',
            field=models.CharField(blank=True, choices=[('hombro', 'Shoulder'), ('codo', 'Elbow'), ('muñeca', 'Wrist'), ('mano', 'Hand'), ('cadera', 'Hip'), ('rodilla', 'Knee'), ('tobillo', 'Ankle'), ('pie', 'Foot'), ('columna_cervical', 'Cervical Spine'), ('columna_dorsal', 'Thoracic Spine'), ('columna_lumbar', 'Lumbar Spine'), ('cuadriceps', 'Quadriceps'), ('isquiotibiales', 'Hamstrings'), ('gemelos', 'Calves'), ('pectoral', 'Pectoral'), ('dorsal', 'Back'), ('trapecio', 'Trapezius'), ('biceps', 'Biceps'), ('triceps', 'Triceps'), ('gluteos', 'Glutes'), ('abdomen', 'Abdomen')], max_length=255),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='NumId',
            field=models.CharField(help_text='Social Security Number or any other recognized mutuality by the state. If unavailable, use NIF or NIE.', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Sexo',
            field=models.CharField(choices=[('M', 'Female'), ('H', 'Male'), ('NS/NR', 'Other')], default='NIF/NIE', max_length=10),
        ),
    ]
