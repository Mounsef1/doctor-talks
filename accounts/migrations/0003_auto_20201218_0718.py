# Generated by Django 3.1.2 on 2020-12-18 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_medecin_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='specialitee',
            field=models.CharField(choices=[('Andrologie', 'Andrologie'), ('Anesthésiologie', 'Anesthésiologie'), ('Cardiologie', ' Cardiologie'), ('Chirurgie cardiaque', ' Chirurgie cardiaque'), ('Chirurgie esthétique,plastique et reconstructive', 'Chirurgie esthétique, plastique et reconstructive'), ('Chirurgie générale', 'Chirurgie générale'), ('Chirurgie maxillo-faciale', 'Chirurgie maxillo-faciale'), ('Chirurgie pédiatrique', 'Chirurgie pédiatrique'), ('Chirurgie thoracique', 'Chirurgie thoracique'), ('Chirurgie vasculaire', 'Chirurgie vasculaire'), ('Dermatologie', 'Dermatologie'), ('Endocrinologie', 'Endocrinologie'), ('Gastro-entérologie', 'Gastro-entérologie'), ('Gynécologie', 'Gynécologie'), ('Gériatrie', 'Gériatrie'), ('Hématologie', 'Hématologie'), ('Hépatologie', 'Hépatologie'), ('Immunologie', 'Immunologie'), ('Infectiologie', 'Infectiologie'), ('Neurochirurgie', 'Neurochirurgie'), ('Neurologie', ' Neurologie'), ('Néonatologie', 'Néonatologie'), ('Néphrologie', 'Néphrologie'), ('Obstétrique', 'Obstétrique'), ('Odontologie', 'Odontologie'), ('Oncologie', 'Oncologie'), ('Ophtalmologie', 'Ophtalmologie'), ('Orthopédie', 'Orthopédie'), ('Oto-rhino-laryngologie', 'Oto-rhino-laryngologie'), ('Pneumologie', 'Pneumologie'), ('Psychiatrie', 'Psychiatrie'), ('Pédiatrie', 'Pédiatrie'), ('Radiologie', 'Radiologie'), ('Radiothérapie', 'Radiothérapie'), ('Rhumatologie', 'Rhumatologie'), ('Urologie', 'Urologie')], max_length=70),
        ),
    ]
