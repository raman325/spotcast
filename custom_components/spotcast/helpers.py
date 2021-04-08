"""Helpers for spotcast."""
import asyncio
import logging
from typing import List
from uuid import UUID
from homeassistant.core import HomeAssistant

import pychromecast

from homeassistant.components.cast.const import DOMAIN as CAST_DOMAIN
from homeassistant.components.zeroconf import async_get_instance
from homeassistant.components.media_player.const import DOMAIN as MP_DOMAIN
from homeassistant.helpers.entity_registry import EntityRegistry

_LOGGER = logging.getLogger(__name__)


def get_spotcast_chromecasts(
    hass: HomeAssistant, ent_reg: EntityRegistry
) -> List[pychromecast.Chromecast]:
    """Get Chromecasts from entity registry."""
    uuids = [
        UUID(entity.unique_id)
        for entity in ent_reg.entities.values()
        if entity.domain == MP_DOMAIN and entity.platform == CAST_DOMAIN
    ]
    _LOGGER.debug("UUIDs found: %s", uuids)

    devices, browser = pychromecast.get_listed_chromecasts(
        uuids=uuids,
        zeroconf_instance=asyncio.run_coroutine_threadsafe(
            async_get_instance(hass), hass.loop
        ).result(),
    )
    browser.stop_discovery()
    _LOGGER.debug("Devices found: %s", devices)

    return devices
