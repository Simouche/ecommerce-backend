# Generated by Django 3.1.4 on 2020-12-29 20:47

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('hex', models.CharField(max_length=9)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='store.subcategory', verbose_name='Category'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
        migrations.AlterField(
            model_name='product',
            name='dimensions',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Dimensions'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Discount Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slider',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='store.Color'),
        ),
    ]