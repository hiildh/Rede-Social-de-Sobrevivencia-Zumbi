from django.db.backends.signals import connection_created
from django.db.backends.postgresql.schema import DatabaseSchemaEditor

class CockroachDBSchemaEditor(DatabaseSchemaEditor):
    sql_create_fk = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s FOREIGN KEY (%(column)s) REFERENCES %(to_table)s (%(to_column)s)"

def disable_deferrable(sender, connection, **kwargs):
    if connection.vendor == 'postgresql':
        connection.SchemaEditorClass = CockroachDBSchemaEditor

connection_created.connect(disable_deferrable)
