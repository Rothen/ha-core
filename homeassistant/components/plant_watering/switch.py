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
    api: PlantWateringAPI = hass.data[DOMAIN][entry.unique_id]
    await api.load_mac_address()

    entities.append(PumpEntity(api, 1))
    # await hass.async_add_executor_job(hass.data[DOMAIN][entry.unique_id].load_mac_address())
    async_add_entities(entities)


class PumpEntity(SwitchEntity):
    """Representation of a Pump."""

    def __init__(self, api: PlantWateringAPI, index: int) -> None:
        """Representation of a Pump."""
        self._api: PlantWateringAPI = api
        self._index = index
        self._is_on = False
        self.entity_id = "switch." + DOMAIN + "_pump_" + str(self._index)

    async def async_update(self) -> None:
        """Update stuff."""
        self._is_on = bool(await self._api.is_pumping(self._index))

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._api.get_mac_address() + "_pump_" + str(self._index)

    @property
    def name(self):
        """Return the name of the entity."""
        return "Pump " + str(self._index)

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self._api.start_pumping(self._index)
        await self.async_update()
        return True

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self._api.stop_pumping(self._index)
        await self.async_update()
        return True
