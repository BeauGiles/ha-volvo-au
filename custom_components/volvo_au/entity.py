"""Common entity base for Volvo AU."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VolvoCoordinator


class VolvoEntity(CoordinatorEntity[VolvoCoordinator]):
    """Common base — every entity shares one DeviceInfo per VIN."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: VolvoCoordinator) -> None:
        super().__init__(coordinator)
        vin = coordinator.client.vin
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, vin)},
            manufacturer="Volvo",
            model="XC40 Recharge",  # could be derived from get_my_cars in v2
            name=f"Volvo {vin}",
        )
