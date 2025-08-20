from django.db import migrations

def create_authors(apps, schema_editor):
    User = apps.get_model('auth', 'User ')
    Author = apps.get_model('News_Portal', 'Author')

    for user in User.objects.all():
        Author.objects.get_or_create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0001_initial'),  # Убедитесь, что это ваша последняя миграция
    ]

    operations = [
        migrations.RunPython(create_authors),
    ]
