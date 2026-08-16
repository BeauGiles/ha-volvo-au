"""Volvo AU button platform — force refresh."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import VolvoCoordinator
from .entity import VolvoEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: VolvoCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VolvoRefreshButton(coordinator), VolvoFlashButton(coordinator), VolvoHonkFlashButton(coordinator)])


class VolvoRefreshButton(VolvoEntity, ButtonEntity):
    _attr_name = "Refresh"
    _attr_icon = "mdi:refresh"

    def __init__(self, coordinator: VolvoCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.client.vin}_refresh"

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()


class VolvoFlashButton(VolvoEntity, ButtonEntity):
    _attr_name = "Flash"
    _attr_icon = "mdi:car-light-high"

    def __init__(self, coordinator: VolvoCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.client.vin}_flash"

    async def async_press(self) -> None:
        await self.coordinator.client.flash()
        self.coordinator.note_command()


class VolvoHonkFlashButton(VolvoEntity, ButtonEntity):
    _attr_name = "Honk & flash"
    _attr_icon = "mdi:bullhorn"

    def __init__(self, coordinator: VolvoCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.client.vin}_honk_flash"

    async def async_press(self) -> None:
        await self.coordinator.client.honk_and_flash()
        self.coordinator.note_command()

