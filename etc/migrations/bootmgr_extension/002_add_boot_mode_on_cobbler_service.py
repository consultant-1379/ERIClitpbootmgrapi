from litp.migration import BaseMigration
from litp.migration.operations import AddProperty


class Migration(BaseMigration):
    version = '2.2.4'
    operations = [AddProperty('cobbler-service', 'boot_mode', 'bios')]
