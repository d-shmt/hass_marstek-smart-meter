"""Config flow for Marstek CT Meter integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import callback

from .const import DOMAIN
from .api import MarstekCtApi, CannotConnect, InvalidAuth

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCAN_INTERVAL = 30

class MarstekCtConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Marstek CT Meter."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}
        if user_input is not None:
            # Kombiniere die Eingaben für den Gerätetyp
            final_data = user_input.copy()
            final_data["device_type"] = f"{user_input['device_type_prefix']}-{user_input['device_type_number']}"
            del final_data["device_type_prefix"]
            del final_data["device_type_number"]

            # Setze die kombinierte Unique ID
            unique_id = f'{final_data["ct_mac"]}_{final_data["battery_mac"]}'
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            try:
                # Validiere die Eingaben
                info = await validate_input(self.hass, final_data)
                return self.async_create_entry(title=info["title"], data=final_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected error during validation")
                errors["base"] = "unknown"
        
        # Schema für die Eingabemaske
        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("battery_mac"): str,
            vol.Required("ct_mac"): str,
            vol.Required("device_type_prefix", default="HMG"): vol.In(["HMG", "HMB", "HMA", "HMK"]),
            vol.Required("device_type_number", default="50"): str,
            vol.Required("ct_type", default="HME-4"): vol.In(["HME-4", "HME-3"]),
        })
        
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for this handler."""
        return MarstekCtOptionsFlow(config_entry)


class MarstekCtOptionsFlow(config_entries.OptionsFlow):
    """Handle an options flow for Marstek CT Meter."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> dict:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Schema für die Options-Maske
        options_schema = vol.Schema({
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=self.config_entry.options.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
            ): vol.All(vol.Coerce(int), vol.Range(min=5)),
        })

        return self.async_show_form(
            step_id="init", data_schema=options_schema
        )

async def validate_input(hass, data: dict) -> dict[str, any]:
    """Validate user input by connecting to the device."""
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
