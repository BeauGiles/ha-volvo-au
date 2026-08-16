"""Volvo (AU) integration setup."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_APP_INSTALLATION_ID,
    CONF_DPOP_PRIVATE_KEY_PEM,
    CONF_REFRESH_TOKEN,
    CONF_VIN,
    DEFAULT_APP_INSTALLATION_ID,
    DOMAIN,
)
from .coordinator import VolvoCoordinator
from .volvo_api import VolvoClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.LOCK,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.TIME,
    Platform.DEVICE_TRACKER,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    data = entry.data
    session = async_get_clientsession(hass)

    client = VolvoClient(
        session,
        vin=data[CONF_VIN],
        dpop_key_pem=data[CONF_DPOP_PRIVATE_KEY_PEM],
        refresh_token=data[CONF_REFRESH_TOKEN],
        app_installation_id=data.get(
            CONF_APP_INSTALLATION_ID, DEFAULT_APP_INSTALLATION_ID
        ),
    )

    # Persist rotated refresh tokens back into the config entry
    def _on_refresh_rotated(new_refresh: str) -> None:
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, CONF_REFRESH_TOKEN: new_refresh},
        )

    client.set_token_updated_callback(_on_refresh_rotated)

    coordinator = VolvoCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
