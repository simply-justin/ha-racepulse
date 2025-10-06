import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, NAME


class F1FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["sensor_name"], data=user_input
            )

        data_schema = vol.Schema(
            {
                vol.Required("sensor_name", default=NAME): cv.string,
                vol.Optional(
                    "live_delay_seconds", default=0
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=300)),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )