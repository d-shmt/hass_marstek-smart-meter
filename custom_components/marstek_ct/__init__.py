"""The Marstek CT Meter integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_MAC, CONF_TYPE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MarstekCtApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Marstek CT Meter from a config entry."""
    
    api = MarstekCtApi(
        host=entry.data[CONF_HOST],
        device_type=entry.data["device_type"],
        battery_mac=entry.data["battery_mac"],
        ct_mac=entry.data[CONF_MAC],
        ct_type=entry.data[CONF_TYPE],
    )

    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            data = await hass.async_add_executor_job(api.fetch_data)
            if "error" in data:
                raise UpdateFailed(f"Error communicating with API: {data['error']}")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="marstek_ct_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
