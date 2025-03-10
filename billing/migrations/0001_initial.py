# Generated by Django 3.2.12 on 2022-05-30 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delta', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Delta')),
                ('expected', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Expected amount')),
                ('reported_at', models.DateTimeField(auto_now_add=True, verbose_name='Reported at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_reports', to='organization.organization', verbose_name='Organization')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='student.student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student Report',
                'verbose_name_plural': 'Student Reports',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_students', models.BigIntegerField(default=0, verbose_name='Total students')),
                ('total_groups', models.BigIntegerField(default=0, verbose_name='Total groups')),
                ('total_income', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='Total income')),
                ('overpayment', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='Overpayment')),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=25, verbose_name='Debt')),
                ('reported_at', models.DateTimeField(auto_now_add=True, verbose_name='Reported at')),
                ('excel', models.FileField(upload_to='reports', verbose_name='Excel')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='organization.organization', verbose_name='Organization')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
    ]
