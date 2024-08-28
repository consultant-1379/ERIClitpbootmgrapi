from litp.core.model_type import ItemType
from litp.core.model_type import Property
from litp.core.model_type import PropertyType
from litp.core.litp_logging import LitpLogger
from litp.core.extension import ModelExtension

log = LitpLogger()


class BootManagerExtension(ModelExtension):
    """
    LITP Model Extension for Boot Manager.
    Allows for the configuration of the Cobbler service on the management
    server.
    Defines the Cobbler service,SELinux mode and Cobbler authentication.
    """

    def define_property_types(self):
        return [
            PropertyType("selinux_mode",
                         regex=r"^(enforcing|permissive|disabled)$"),
            PropertyType("cobbler_authentication",
                         regex=r"^(authn_configfile|authn_testing)$"),
            PropertyType('boot_mode',
                         regex=r"^(uefi|bios)$")
        ]

    def define_item_types(self):
        return [
            ItemType(
                "cobbler-service",
                item_description=("This item type represents "
                                  "a Cobbler service."),
                extend_item="service-base",
                puppet_auto_setup=Property(
                    "basic_boolean",
                    default="true",
                    prop_description=("Ensure that Puppet "
                                      "is installed during machine provision.")
                ),
                sign_puppet_certs_automatically=Property(
                    "basic_boolean",
                    default="true",
                    prop_description=("Ensure Cobbler signs Puppet "
                                      "certs automatically.")
                ),
                remove_old_puppet_certs_automatically=Property(
                    "basic_boolean",
                    default="true",
                    prop_description=("Ensure that Cobbler removes old "
                                      "Puppet certs automatically.")
                ),
                manage_dhcp=Property(
                    "basic_boolean",
                    default="true",
                    prop_description=("Allow Cobbler to manage a "
                                      "local DHCP server.")
                ),
                manage_dns=Property(
                    "basic_boolean",
                    default="false",
                    prop_description=("Enable Cobbler's DHCP "
                                      "management features")
                ),
                authentication=Property(
                    "cobbler_authentication",
                    default='authn_configfile',
                    prop_description="Cobbler authentication method."
                ),
                rsync_disabled=Property(
                    "basic_boolean",
                    default="false",
                    prop_description="Disable Cobbler rsync."
                ),
                ksm_selinux_mode=Property(
                    "selinux_mode",
                    default='enforcing',
                    prop_description=("The selinux security policy "
                                      "within the kickstart file.")
                ),
                ksm_path=Property(
                    "file_path_string",
                    default='/var/lib/cobbler/kickstarts',
                    prop_description=("Location where the kickstart "
                                      "file is placed.")
                ),
                ksm_ksname=Property(
                    "basic_string",
                    default='litp.ks',
                    prop_description="The name of the kickstart file."
                ),
                pxe_boot_timeout=Property(
                    "positive_integer",
                    prop_description=("Maximum time in seconds to wait for a "
                                      "peer server to PXE boot"),
                    required=False,
                    default="600"
                ),
                boot_mode=Property(
                    "boot_mode",
                    required=True,
                    default="bios",
                    prop_description="Boot mode (uefi|bios).",
                    site_specific=True
                ),
            ),
        ]

    @staticmethod
    def _get_cobbler_service(plugin_api_context):
        services = plugin_api_context.query("cobbler-service")
        if not services:
            log.trace.debug("No cobbler service found")
            return None
        return services[0]
