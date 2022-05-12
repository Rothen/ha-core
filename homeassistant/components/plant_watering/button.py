"""The Plant Watering integration."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PlantWateringAPI
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Abode binary sensor devices."""
    entities = []
    entities.append(MySwitch(hass.data[DOMAIN][entry.unique_id]))
    async_add_entities(entities)


class MySwitch(SwitchEntity):
    """Representation of a Pump."""

    def __init__(self, api: PlantWateringAPI) -> None:
        """Representation of a Pump."""
        self._api = api
        self._is_on = False

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._api.get_mac_address() + "_pump"

    @property
    def name(self):
        """Return the name of the entity."""
        return "My Switch"

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
