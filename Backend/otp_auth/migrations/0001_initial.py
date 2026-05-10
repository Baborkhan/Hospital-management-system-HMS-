from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='EmailOTP',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email',         models.EmailField(db_index=True, max_length=254)),
                ('otp',           models.CharField(max_length=6)),
                ('created_at',    models.DateTimeField(auto_now_add=True)),
                ('expires_at',    models.DateTimeField()),
                ('is_used',       models.BooleanField(default=False)),
                ('attempt_count', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'mf_email_otp',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['email', 'is_used'], name='mf_email_otp_email_is_used_idx')],
            },
        ),
    ]

