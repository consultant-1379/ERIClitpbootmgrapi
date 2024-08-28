#############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
#############################################################################

import re
import unittest

from bootmgr_extension.bootmgr_extension import BootManagerExtension

from litp.extensions.core_extension import CoreExtension
from litp.core.model_manager import ModelManager
from litp.core.plugin_manager import PluginManager
from litp.core.plugin_context_api import PluginApiContext


class TestBootManagerExtension(unittest.TestCase):

    def setUp(self):
        self.ext = BootManagerExtension()

        self.model_manager = ModelManager()
        self.validator = self.model_manager.validator
        self.plugin_manager = PluginManager(self.model_manager)
        self.context = PluginApiContext(self.model_manager)

        # add the core and boot manager extensions to the plugin manager
        for ext in [CoreExtension(), BootManagerExtension()]:
            self.plugin_manager.add_property_types(ext.define_property_types())
            self.plugin_manager.add_item_types(ext.define_item_types())
            if isinstance(ext, CoreExtension):
                self.plugin_manager.add_default_model()

    def test_property_types_registered(self):
        prop_types_expected = ['selinux_mode',
                               'cobbler_authentication',
                               'boot_mode']
        prop_types = [pt.property_type_id for pt in
                      self.ext.define_property_types()]
        self.assertEquals(prop_types_expected, prop_types)

    def test_item_types_registered(self):
        item_types_expected = ['cobbler-service']
        item_types = [it.item_type_id for it in
                      self.ext.define_item_types()]
        self.assertEquals(item_types_expected, item_types)

    def test_authentication_regex(self):
        
        auth_regex = [pt.regex for pt in self.ext.define_property_types() \
                      if pt.property_type_id is 'cobbler_authentication']
        self.assertNotEquals(re.match(auth_regex[0], 'authn_configfile'), None)
        self.assertNotEquals(re.match(auth_regex[0], 'authn_testing'), None)
        self.assertEquals(re.match(auth_regex[0], 'blah'), None)
        self.assertEquals(re.match(auth_regex[0], 'authn_testingrubbish'), None)
        
    def test_selinux_regex(self):
        
        auth_regex = [pt.regex for pt in self.ext.define_property_types() \
                      if pt.property_type_id is 'selinux_mode']
        self.assertNotEquals(re.match(auth_regex[0], 'enforcing'), None)
        self.assertNotEquals(re.match(auth_regex[0], 'permissive'), None)
        self.assertNotEquals(re.match(auth_regex[0], 'disabled'), None)
        self.assertEquals(re.match(auth_regex[0], 'blah'), None)
        self.assertEquals(re.match(auth_regex[0], 'enforcinghh'), None)

    def test_invalid_pxe_boot_timeout_value(self):

        self.model_manager.create_core_root_items()

        deployment = self.model_manager.create_item(
            'deployment',
            '/deployments/d1'
        )
        cluster = self.model_manager.create_item(
            'cluster',
            '/deployments/d1/clusters/c1'
        )

        # probably should be a node item
        system = self.model_manager.create_item(
            'system',
            '/infrastructure/systems/s0',
            system_name='MS1'
        )
        cobbler_service = self.model_manager.create_item(
            'cobbler-service',
            '/ms/services/cobbler'
        )

        for item in [deployment, cluster, system, cobbler_service]:
            item.set_applied()

        neg_values = ['-1', '0', '-600', '42.5', '-42.5', '0100', 'foo']

        for value in neg_values:
            errors = self.model_manager.update_item(
                '/ms/services/cobbler',
                pxe_boot_timeout=value
            )

            self.assertEqual(1, len(errors))
            self.assertEqual('ValidationError', errors[0].error_type)

            expected_error = "Invalid value '{0}'.".format(value)
            self.assertEqual(expected_error, errors[0].error_message)

        pos_values = ['1', '42', '120', '3000']

        for value in pos_values:
            updated_item = self.model_manager.update_item(
                '/ms/services/cobbler',
                pxe_boot_timeout=value
            )

            self.assertEquals('Updated', updated_item.get_state())

if __name__ == '__main__':
    unittest.main()
