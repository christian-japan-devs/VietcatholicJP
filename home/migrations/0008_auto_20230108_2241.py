# Generated by Django 3.2.16 on 2023-01-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20230108_2138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='youtubevideo',
            options={'ordering': ['created_on', 'title'], 'verbose_name': 'Youtube video', 'verbose_name_plural': 'Youtube videos'},
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='excerpt',
            field=models.TextField(blank=True, default='', help_text='Không quá 500 ký tự', max_length=500, null=True, verbose_name='Tóm tắt'),
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='youtube_url',
            field=models.CharField(help_text='Lưu ý là id của video link phần XXXXXXXXX từ sau ?v=XXXXXXXXX', max_length=200, verbose_name='Youtube id'),
        ),
    ]
