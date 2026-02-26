"""The Marstek CT Meter integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import MarstekCtApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
# Die BINARY_SENSOR-Plattform wird hier wieder entfernt
PLATFORMS: list[Platform] = [Platform.SENSOR]

FIRST_REFRESH_TIMEOUT = 10.0
BASE_UPDATE_INTERVAL = timedelta(seconds=5)
MAX_BACKOFF_INTERVAL = timedelta(seconds=60)
BACKOFF_FACTOR = 2

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Marstek CT Meter from a config entry."""
    api = MarstekCtApi(
        host=entry.data["host"],
        device_type=entry.data["device_type"],
        battery_mac=entry.data["battery_mac"],
        ct_mac=entry.data["ct_mac"],
        ct_type=entry.data["ct_type"],
    )

    consecutive_failures = 0
    coordinator: DataUpdateCoordinator | None = None

    def _apply_backoff() -> None:
        """Apply exponential backoff to the coordinator update interval."""
        if coordinator is None:
            return
        if consecutive_failures <= 0:
            new_interval = BASE_UPDATE_INTERVAL
        else:
            backoff_seconds = BASE_UPDATE_INTERVAL.total_seconds() * (
                BACKOFF_FACTOR ** (consecutive_failures - 1)
            )
            new_interval = timedelta(
                seconds=min(backoff_seconds, MAX_BACKOFF_INTERVAL.total_seconds())
            )
        if coordinator.update_interval != new_interval:
            coordinator.update_interval = new_interval

    async def async_update_data():
        """Fetch data from API endpoint."""
        nonlocal consecutive_failures
        try:
            data = await asyncio.wait_for(
                hass.async_add_executor_job(api.fetch_data),
                timeout=FIRST_REFRESH_TIMEOUT,
            )
        except asyncio.TimeoutError as err:
            consecutive_failures += 1
            _apply_backoff()
            _LOGGER.debug(
                "Timeout while communicating with API (failures=%d)",
                consecutive_failures,
            )
            return {"error": f"Timeout while communicating with API: {err}"}

        if "error" in data:
            consecutive_failures += 1
            _apply_backoff()
            _LOGGER.debug(
                "API error response (failures=%d): %s",
                consecutive_failures,
                data["error"],
            )
            return data

        if consecutive_failures:
            consecutive_failures = 0
            _apply_backoff()
        return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="marstek_ct_sensor",
        update_method=async_update_data,
        update_interval=BASE_UPDATE_INTERVAL,
    )

    _apply_backoff()
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
