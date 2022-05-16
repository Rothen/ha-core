"""The Plant Watering integration."""
from __future__ import annotations

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]


class PlantWateringAPI:
    """PlantWateringAPI."""

    def __init__(self, host: str) -> None:
        """PlantWateringAPI."""
        self._host = host
        self._mac_address = ""

    async def _get(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def _put(self, url: str, json: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=json) as resp:
                return await resp.json()

    async def _delete(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as resp:
                return await resp.json()

    async def load_mac_address(self) -> str:
        """Return the mac address."""
        data = await self._get("http://" + self._host + "/about")
        self._mac_address = data["mac_address"]
        return self._mac_address

    def get_mac_address(self) -> str:
        """Return the Moisture."""
        return self._mac_address

    async def get_moisture(self, index: int) -> str:
        """Return the Moisture."""
        data = await self._get("http://" + self._host + "/moisture/" + str(index))
        return data["value"]

    async def start_pumping(self, index: int) -> None:
        """Return the Moisture."""
        await self._put(
            "http://" + self._host + "/pump/" + str(index), {"duration": 10000}
        )

    async def stop_pumping(self, index: int) -> None:
        """Return the Moisture."""
        await self._delete("http://" + self._host + "/pump/" + str(index))

    async def is_pumping(self, index: int) -> bool:
        """Return the Moisture."""
        data = await self._get("http://" + self._host + "/pump/" + str(index))
        return data["is_pumping"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Plant Watering from a config entry."""
    api = PlantWateringAPI(entry.data["host"])
    await api.load_mac_address()
    entry.unique_id = api.get_mac_address()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.unique_id] = api

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
