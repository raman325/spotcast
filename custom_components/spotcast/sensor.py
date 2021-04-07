from datetime import timedelta
import json
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_registry import async_get
from homeassistant.util import dt
from homeassistant.const import STATE_OK, STATE_UNKNOWN

from .helpers import get_spotcast_chromecasts

_LOGGER = logging.getLogger(__name__)

SENSOR_SCAN_INTERVAL_SECS = 10
SCAN_INTERVAL = timedelta(seconds=SENSOR_SCAN_INTERVAL_SECS)


def setup_platform(hass, config, add_devices, discovery_info=None):
    _LOGGER.error("test")
    entity = ChromecastDevicesSensor(hass)
    add_devices([entity])
    _LOGGER.error(entity.unique_id)

class ChromecastDevicesSensor(Entity):

    def __init__(self, hass):
        self.hass = hass
        self._state = STATE_UNKNOWN
        self._chromecast_devices = []
        self._attributes = {
            'devices_json': [],
            'devices': [],
            'last_update': None
        }
        self.ent_reg = None
        _LOGGER.debug('initiating sensor')

    async def async_added_to_hass(self) -> None:
        self.ent_reg = async_get(self.hass)

    @property
    def name(self):
        return 'Chromecast Devices'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        _LOGGER.debug('Getting chromecast devices')

        known_devices = get_spotcast_chromecasts(self.ent_reg)

        _LOGGER.debug('devices %s', known_devices)

        chromecasts = [
            {
                "host": str(k.socket_client.host),
                "port": k.socket_client.port,
                "uuid": str(k.uuid),
                "model_name": k.model_name,
                "name": k.device.friendly_name,
                'manufacturer': k.device.manufacturer
            }
            for k in known_devices
        ]

        self._attributes['devices_json'] = json.dumps(chromecasts, ensure_ascii=False)
        self._attributes['devices'] = chromecasts
        self._attributes['last_update'] = dt.now().isoformat('T')
        self._state = STATE_OK



