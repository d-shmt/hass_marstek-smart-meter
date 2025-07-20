"""Config flow for Marstek CT Meter integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_MAC, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN
from .api import MarstekCtApi, CannotConnect, InvalidAuth

# Erstellt eine Instanz des Loggers
_LOGGER = logging.getLogger(__name__)

# Schema für die Eingabemaske in der UI
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required("battery_mac"): str,
        vol.Required(CONF_MAC): str,
        vol.Required("device_type", default="HMG-50"): str,
        vol.Required(CONF_TYPE, default="HME-4"): vol.In(["HME-4", "HME-3"]),
    }
)

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, any]:
    """Prüft die Benutzereingaben auf Gültigkeit."""
    api = MarstekCtApi(
        host=data[CONF_HOST],
        device_type=data["device_type"],
        battery_mac=data["battery_mac"],
        ct_mac=data[CONF_MAC],
        ct_type=data[CONF_TYPE],
    )

    result = await hass.async_add_executor_job(api.test_connection)
    
    if "error" in result:
        error_msg = result["error"]
        if "Timeout" in error_msg:
            raise CannotConnect(error_msg)
        else:
            raise InvalidAuth(error_msg)
            
    return {"title": f"Marstek CT {data[CONF_HOST]}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Verwaltet den Konfigurations-Flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Behandelt den ersten Schritt des Flows."""
        errors = {}
        if user_input is not None:
            # Verhindert, dass das gleiche Gerät mehrfach hinzugefügt wird
            unique_id = format_mac(user_input[CONF_MAC])
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                # DIES IST DIE ENTSCHEIDENDE NEUE ZEILE:
                # Sie schreibt den vollständigen Fehler ins Protokoll.
                _LOGGER.exception("Unerwarteter Fehler bei der Validierung")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )