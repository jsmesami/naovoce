from django.db import migrations


SQL = """
UPDATE fruit_herbarium h SET new_url = 'https://na-ovoce.cz/web/herbar#' || k.key
FROM fruit_kind k WHERE k.id = h.kind_id
"""


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0006_herbarium_new_url'),
    ]
    url = ''
    operations = [
        migrations.RunSQL(SQL)
    ]
