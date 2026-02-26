"""Sensor platform for Marstek CT Meter."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="total_power",
        translation_key="total_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery_power",
        translation_key="battery_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="wifi_rssi",
        translation_key="wifi_rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="A_phase_power",
        translation_key="a_phase_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="B_phase_power",
        translation_key="b_phase_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="C_phase_power",
        translation_key="c_phase_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(key="meter_dev_type", translation_key="meter_dev_type", entity_registry_enabled_default=False),
    SensorEntityDescription(key="meter_mac_code", translation_key="meter_mac_code", entity_registry_enabled_default=False),
    SensorEntityDescription(key="hhm_dev_type", translation_key="hhm_dev_type", entity_registry_enabled_default=False),
    SensorEntityDescription(key="hhm_mac_code", translation_key="hhm_mac_code", entity_registry_enabled_default=False),
    SensorEntityDescription(key="info_idx", translation_key="info_idx", entity_registry_enabled_default=False),
    SensorEntityDescription(key="A_chrg_nb", translation_key="a_chrg_nb", icon="mdi:numeric-1-box-multiple-outline", entity_registry_enabled_default=False),
    SensorEntityDescription(key="B_chrg_nb", translation_key="b_chrg_nb", icon="mdi:numeric-1-box-multiple-outline", entity_registry_enabled_default=False),
    SensorEntityDescription(key="C_chrg_nb", translation_key="c_chrg_nb", icon="mdi:numeric-1-box-multiple-outline", entity_registry_enabled_default=False),
    SensorEntityDescription(
        key="ABC_chrg_nb",
        translation_key="abc_chrg_nb",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="x_chrg_power",
        translation_key="x_chrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="A_chrg_power",
        translation_key="a_chrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="B_chrg_power",
        translation_key="b_chrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="C_chrg_power",
        translation_key="c_chrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="ABC_chrg_power",
        translation_key="abc_chrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="x_dchrg_power",
        translation_key="x_dchrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="A_dchrg_power",
        translation_key="a_dchrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="B_dchrg_power",
        translation_key="b_dchrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="C_dchrg_power",
        translation_key="c_dchrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="ABC_dchrg_power",
        translation_key="abc_dchrg_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [MarstekCtSensor(coordinator, description, entry) for description in SENSOR_DESCRIPTIONS]
    async_add_entities(entities)


class MarstekCtSensor(CoordinatorEntity, SensorEntity):
    """Marstek CT Meter Sensor."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, description: SensorEntityDescription, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry

        # Fallbacks: Entry-Daten sind stabil, Coordinator kann beim Boot leer/fehlerhaft sein
        ct_mac = (coordinator.data or {}).get("meter_mac_code") or entry.data.get("ct_mac") or "unknown_ct"
        battery_mac = entry.data.get("battery_mac") or "unknown_batt"

        self._ct_mac = ct_mac
        self._battery_mac = battery_mac

        self._attr_unique_id = f"{ct_mac}_{battery_mac}_{description.key}"

        device_identifier = f"{ct_mac}_{battery_mac}"
        model = (coordinator.data or {}).get("meter_dev_type") or "Marstek CT"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_identifier)},
            "name": f"Marstek CT {ct_mac[-4:]} / Battery {battery_mac[-4:]}",
            "manufacturer": "Marstek",
            "model": model,
        }

    @property
    def available(self) -> bool:
        """Mark entity unavailable when API returns an error."""
        data = self.coordinator.data
        if not isinstance(data, dict):
            return False
        if "error" in data:
            return False
        return True

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        data = self.coordinator.data or {}
        return data.get(self.entity_description.key)
