"""Sensor platform for Marstek CT Meter."""
from __future__ import annotations
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

# Sensoren werden über ihren 'key' definiert.
# Der Name kommt aus den Übersetzungsdateien.
SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="total_power", 
        translation_key="total_power", 
        device_class=SensorDeviceClass.POWER, 
        native_unit_of_measurement=UnitOfPower.WATT, 
        state_class=SensorStateClass.MEASUREMENT
    ),
    SensorEntityDescription(
        key="wifi_rssi", 
        translation_key="wifi_rssi", 
        device_class=SensorDeviceClass.SIGNAL_STRENGTH, 
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT, 
        state_class=SensorStateClass.MEASUREMENT
    ),
    # KORREKTUR: Die 'key'-Einträge müssen mit den API-Daten übereinstimmen (Großbuchstaben)
    SensorEntityDescription(
        key="A_phase_power", 
        translation_key="a_phase_power", 
        device_class=SensorDeviceClass.POWER, 
        native_unit_of_measurement=UnitOfPower.WATT, 
        state_class=SensorStateClass.MEASUREMENT
    ),
    SensorEntityDescription(
        key="B_phase_power", 
        translation_key="b_phase_power", 
        device_class=SensorDeviceClass.POWER, 
        native_unit_of_measurement=UnitOfPower.WATT, 
        state_class=SensorStateClass.MEASUREMENT
    ),
    SensorEntityDescription(
        key="C_phase_power", 
        translation_key="c_phase_power", 
        device_class=SensorDeviceClass.POWER, 
        native_unit_of_measurement=UnitOfPower.WATT, 
        state_class=SensorStateClass.MEASUREMENT
    ),
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [MarstekCtSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS]
    async_add_entities(entities)

class MarstekCtSensor(CoordinatorEntity, SensorEntity):
    """Marstek CT Meter Sensor."""
    _attr_has_entity_name = True

    def __init__(self, coordinator, description: SensorEntityDescription):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data['meter_mac_code']}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.data["meter_mac_code"])},
            "name": f"Marstek CT {coordinator.data['meter_mac_code'][-4:]}",
            "manufacturer": "Marstek",
            "model": coordinator.data["meter_dev_type"],
        }
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)
