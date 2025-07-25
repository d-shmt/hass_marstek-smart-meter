"""Config flow for Marstek CT Meter integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN
from .api import MarstekCtApi, CannotConnect, InvalidAuth

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("battery_mac"): str,
        vol.Required("ct_mac"): str,
        vol.Required("device_type_prefix", default="HMG"): vol.In(["HMG", "HMB", "HMA", "HMK"]),
        vol.Required("device_type_number", default="50"): str,
        vol.Required("ct_type", default="HME-4"): vol.In(["HME-4", "HME-3"]),
    }
)

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, any]:
    """Prüft die Benutzereingaben auf Gültigkeit."""
    api = MarstekCtApi(
        host=data["host"],
        device_type=data["device_type"],
        battery_mac=data["battery_mac"],
        ct_mac=data["ct_mac"],
        ct_type=data["ct_type"],
    )
    result = await hass.async_add_executor_job(api.test_connection)
    if "error" in result:
        error_msg = result["error"]
        if "Timeout" in error_msg:
            raise CannotConnect(error_msg)
        else:
            raise InvalidAuth(error_msg)
    return {"title": f"Marstek CT {data['host']}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Verwaltet den Konfigurations-Flow."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Behandelt den ersten Schritt des Flows."""
        errors = {}
        if user_input is not None:
            final_data = user_input.copy()
            final_data["device_type"] = f"{user_input['device_type_prefix']}-{user_input['device_type_number']}"
            
            del final_data["device_type_prefix"]
            del final_data["device_type_number"]

            # ===================================================================
            # HIER IST DIE ÄNDERUNG: Die Unique ID wird aus beiden MACs gebildet
            # ===================================================================
            unique_id = f'{format_mac(final_data["ct_mac"])}_{format_mac(final_data["battery_mac"])}'
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()
            # ===================================================================

            try:
                info = await validate_input(self.hass, final_data)
                return self.async_create_entry(title=info["title"], data=final_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unerwarteter Fehler bei der Validierung")
                errors["base"] = "unknown"
        
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
