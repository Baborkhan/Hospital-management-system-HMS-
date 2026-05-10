from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('session_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('user_id', models.CharField(blank=True, max_length=64, null=True)),
                ('user_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('turn_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'app_label': 'ai'},
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='ai.chatsession')),
                ('role', models.CharField(choices=[('user','User'),('assistant','Assistant')], max_length=12)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('urgency', models.CharField(blank=True, max_length=20)),
                ('specialist', models.CharField(blank=True, max_length=80)),
                ('is_emergency', models.BooleanField(default=False)),
            ],
            options={'app_label': 'ai', 'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('user_id', models.CharField(db_index=True, default='anonymous', max_length=64)),
                ('bp', models.CharField(blank=True, max_length=20)),
                ('hr', models.CharField(blank=True, max_length=20)),
                ('bmi', models.FloatField(blank=True, null=True)),
                ('systolic', models.IntegerField(blank=True, null=True)),
                ('diastolic', models.IntegerField(blank=True, null=True)),
                ('sugar', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={'app_label': 'ai', 'ordering': ['-created_at']},
        ),
    ]

