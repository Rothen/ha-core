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
    api: PlantWateringAPI = hass.data[DOMAIN][entry.unique_id]
    await api.load_mac_address()
    entities.append(ExampleSensor(api, 1))
    async_add_entities(entities)


class ExampleSensor(SensorEntity):
    """Representation of a Moisture Sensor."""

    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, api: PlantWateringAPI, index: int) -> None:
        """Representation of a Pump."""
        self._api = api
        self._index = index
        self._attr_name = "Moisture Sensor " + str(self._index)
        self.entity_id = "sensor." + DOMAIN + "_moisture_" + str(self._index)
        self._attr_unique_id = (
            self._api.get_mac_address() + ".moisture_sensor_" + str(self._index)
        )

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = await self._api.get_moisture(self._index)
