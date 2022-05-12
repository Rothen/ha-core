"""Something."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PlantWateringAPI
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Abode binary sensor devices."""
    entities = []
    entities.append(ExampleSensor(api=hass.data[DOMAIN][entry.unique_id]))
    async_add_entities(entities)


class ExampleSensor(SensorEntity):
    """Representation of a Moisture Sensor."""

    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, api: PlantWateringAPI) -> None:
        """Representation of a Pump."""
        self._api = api
        self._attr_unique_id = self._api.get_mac_address() + ".moisture_sensor"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self._api.get_moisture()
