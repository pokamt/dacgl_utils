# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-22 12:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Mobilier,info,élec,...', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('valeur', models.PositiveIntegerField()),
                ('section', models.CharField(choices=[('INF', 'COM-INF'), ('ARE', 'COM-ARE')], default='INF', max_length=10)),
                ('numero', models.PositiveIntegerField()),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Devise',
            fields=[
                ('identifiant', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ensemble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(default='Piece', max_length=200)),
                ('description', models.TextField(blank=True)),
                ('prix_achat', models.PositiveIntegerField()),
                ('fonctionnel', models.BooleanField(default=True)),
                ('usage', models.CharField(choices=[('personnel', 'Personnel'), ('infrastructure', 'Infrastructure'), ('usager', 'Usager'), ('projet', 'Projet')], default='personnel', max_length=20)),
                ('commentaire', models.TextField(blank=True)),
                ('emplacement', models.CharField(blank=True, max_length=200)),
                ('reserve', models.BooleanField(default=False)),
                ('sortie', models.BooleanField(default=False, help_text='Sortie de stock ?')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Categorie')),
                ('devise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Devise')),
            ],
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(help_text='Quel famille de produits ? ordi,imprimante', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Marque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_serie', models.CharField(max_length=200, unique=True, verbose_name='Numéro de série')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('date_acquisition', models.DateField()),
                ('code_inventaire', models.CharField(max_length=100, unique=True)),
                ('comm_coda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Commande')),
                ('ensemble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Ensemble')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modele', models.CharField(max_length=100)),
                ('constructeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Marque')),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Famille')),
            ],
        ),
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom structure')),
                ('adresse', models.TextField(verbose_name='Adresse physique')),
                ('description', models.TextField(verbose_name='Description sommaire')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('telephone', models.IntegerField(blank=True, null=True)),
                ('site_web', models.URLField(blank=True)),
                ('id_CODA', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='piece',
            name='modele',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Produit'),
        ),
        migrations.AddField(
            model_name='ensemble',
            name='ville',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Ville'),
        ),
        migrations.AddField(
            model_name='commande',
            name='devise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Devise'),
        ),
        migrations.AddField(
            model_name='commande',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaire.Societe'),
        ),
        migrations.AlterUniqueTogether(
            name='commande',
            unique_together=set([('section', 'numero')]),
        ),
    ]
