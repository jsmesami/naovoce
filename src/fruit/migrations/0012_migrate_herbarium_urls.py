from django.db import migrations


SQL = """
UPDATE fruit_herbarium h SET new_url = 'https://www.na-ovoce.cz/herbar#' || k.key
FROM fruit_kind k WHERE k.id = h.kind_id
"""


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0011_kind_deleted'),
    ]
    url = ''
    operations = [
        migrations.RunSQL(SQL)
    ]
