from litp.migration import BaseMigration
from litp.migration.operations import AddProperty


class Migration(BaseMigration):
    version = '1.18.1'
    operations = [
        AddProperty('cobbler-service', 'pxe_boot_timeout', '600'),
    ]
