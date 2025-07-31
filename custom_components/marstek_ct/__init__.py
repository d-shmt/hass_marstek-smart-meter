"""The Marstek CT Meter integration."""
from __future__ import annotations
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import MarstekCtApi
from .const import DOMAIN
from .options_flow import async_get_options_flow # Wichtig: Import des Options-Flows

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]
DEFAULT_SCAN_INTERVAL = 30

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Marstek CT Meter from a config entry."""
    
    # Registriere den Options-Flow
    entry.async_get_options_flow = async_get_options_flow
    
    # Lese das Update-Intervall aus den Optionen, mit Fallback auf den Standardwert
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    api = MarstekCtApi(
        host=entry.data["host"],
        device_type=entry.data["device_type"],
        battery_mac=entry.data["battery_mac"],
        ct_mac=entry.data["ct_mac"],
        ct_type=entry.data["ct_type"],
    )

    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            data = await hass.async_add_executor_job(api.fetch_data)
            if "error" in data:
                raise UpdateFailed(f"API error: {data['error']}")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="marstek_ct_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=scan_interval), # Verwende den konfigurierbaren Wert
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Füge einen Listener hinzu, der auf Options-Änderungen reagiert
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle an options update."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
