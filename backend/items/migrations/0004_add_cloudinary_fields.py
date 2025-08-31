# Generated migration for cloudinary_public_ids field

from django.db import migrations, models
from django.contrib.postgres.fields import ArrayField

class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_alter_item_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cloudinary_public_ids',
            field=ArrayField(
                models.CharField(max_length=200),
                size=10,
                default=list,
                blank=True,
                help_text="Cloudinary public IDs for image management"
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_urls',
            field=ArrayField(
                models.CharField(max_length=500),
                size=10,
                default=list,
                blank=True,
                help_text="Cloudinary image URLs"
            ),
        ),
    ]
