"""Config flow for Marstek CT Meter integration."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN
from .api import MarstekCtApi, CannotConnect

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required("battery_mac"): str,
        vol.Required("ct_mac"): str,
        vol.Required("device_type_prefix", default="HMG"): vol.In(["HMG", "HMB", "HMA", "HMK"]),
        vol.Required("device_type_number", default="50"): str,
        vol.Required("ct_type", default="HME-4"): vol.In(["HME-4", "HME-3"]),
    }
)

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input."""
    # Normalize MACs early for consistent payload and stable unique_id behavior
    data = dict(data)
    data["battery_mac"] = format_mac(data["battery_mac"])
    data["ct_mac"] = format_mac(data["ct_mac"])

    api = MarstekCtApi(
        host=data[CONF_HOST],
        device_type=data["device_type"],
        battery_mac=data["battery_mac"],
        ct_mac=data["ct_mac"],
        ct_type=data["ct_type"],
    )

    result = await hass.async_add_executor_job(api.test_connection)
    if isinstance(result, dict) and "error" in result:
        raise CannotConnect(result["error"])

    return {"title": f"Marstek CT {data[CONF_HOST]}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the integration."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            final_data = dict(user_input)
            final_data["device_type"] = f"{final_data['device_type_prefix']}-{final_data['device_type_number']}"
            final_data.pop("device_type_prefix", None)
            final_data.pop("device_type_number", None)

            # Unique ID from both MACs (normalized)
            unique_id = f"{format_mac(final_data['ct_mac'])}_{format_mac(final_data['battery_mac'])}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, final_data)
                return self.async_create_entry(title=info["title"], data=final_data)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during validation")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
