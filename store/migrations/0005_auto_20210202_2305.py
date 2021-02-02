# Generated by Django 3.1.4 on 2021-02-02 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210115_1028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, related_name='products', to='store.Color'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slider',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
