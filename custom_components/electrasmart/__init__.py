"""Support for Electra Smart air conditioners."""
from __future__ import annotations

import logging
from typing import cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from pyelectrasmart import ElectraAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "electrasmart"
PLATFORMS: list[Platform] = [Platform.CLIMATE]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Electra Smart from a config entry."""
    _LOGGER.debug(
        "Setting up Electra Smart entry '%s' (configured keys: %s)",
        entry.entry_id,
        list(entry.data.keys()),
    )

    # Instantiate API client
    api = ElectraAPI(
        entry.data.get("imei"),
        entry.data.get("token"),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    try:
        _LOGGER.debug("Fetching Electra devices from cloud API...")
        await api.fetch_devices()

        devices = getattr(api, "devices", None) or getattr(api, "air_conditioners", [])
        _LOGGER.info("Discovered %d Electra device(s)", len(devices))
        for dev in devices:
            _LOGGER.debug(
                "Device: name=%s, id=%s, model=%s",
                getattr(dev, "name", "Unknown"),
                getattr(dev, "id", "Unknown"),
                getattr(dev, "model", "Unknown"),
            )

    except KeyError as err:
        _LOGGER.error(
            "Electra API payload schema mismatch (KeyError: %s). "
            "Electra has updated their backend API payload structure.",
            err,
            exc_info=True,
        )
        raise ConfigEntryNotReady(f"Electra API schema changed: missing key {err}") from err

    except Exception as err:
        _LOGGER.error("Failed to connect or fetch devices from Electra: %s", err, exc_info=True)
        raise ConfigEntryNotReady(f"Could not connect to Electra cloud: {err}") from err

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

