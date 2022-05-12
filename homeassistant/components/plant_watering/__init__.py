"""The Plant Watering integration."""
from __future__ import annotations

import requests

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]


class PlantWateringAPI:
    """PlantWateringAPI."""

    def __init__(self, host: str, mac_address: str) -> None:
        """PlantWateringAPI."""
        self._host = host
        self._mac_address = mac_address

    def get_mac_address(self) -> str:
        """Return the mac address."""
        return self._mac_address

    def get_moisture(self) -> int:
        """Return the Moisture."""
        res = requests.get("http://" + self._host + "/moisture/1")
        return res.json()["value"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Plant Watering from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    entry.unique_id = "e5:77:1a:2f:51:ef"
    hass.data[DOMAIN][entry.unique_id] = PlantWateringAPI(
        entry.data["host"], entry.unique_id
    )

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
