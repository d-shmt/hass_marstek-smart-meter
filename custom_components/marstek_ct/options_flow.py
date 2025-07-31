"""Options flow for Marstek CT Meter."""
from __future__ import annotations
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigEntry, OptionsFlow
from homeassistant.core import callback
from homeassistant.const import CONF_SCAN_INTERVAL

from .const import DOMAIN

DEFAULT_SCAN_INTERVAL = 30

class MarstekCtOptionsFlow(OptionsFlow):
    """Handle an options flow for Marstek CT Meter."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> dict:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5)),
                }
            ),
        )

# Dieser Teil wird benötigt, um den Options-Flow zu registrieren
@callback
def async_get_options_flow(config_entry: ConfigEntry) -> MarstekCtOptionsFlow:
    """Get the options flow for this handler."""
    return MarstekCtOptionsFlow(config_entry)
