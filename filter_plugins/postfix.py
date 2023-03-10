# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'type': self.var_type,
            'validate_tls': self.validate_tls,
            'is_value': self.value,
            'postfix_map_data': self.map_data,
            'valid_list_data': self.valid_list_data,
        }

    def var_type(self, var):
        """
          Get the type of a variable
        """
        return type(var).__name__

    def validate_tls(self, data, type="cert"):
        """
        """
        msg = "failed, because ... tree"
        result = dict(
            valid = False,
            msg = msg
        )

        return result

    def value(self, data):
        """
        """
        result = None
        # display.v(f"value({data} {type(data)})")

        if isinstance(data, bool):
            result = 'yes' if data else 'no'
        elif isinstance(data, str):
            if len(data) > 0:
                result = data
        elif isinstance(data, int):
            result = data

        # display.v(f"= result: {result} {type(result)}")

        return result

    def map_data(self, data):
        """
        """
        # display.v(f"value({data} {type(data)})")

        key = None
        values = None

        if isinstance(data, dict):
            key = data[list(data.keys())[0]]
            values = data[list(data.keys())[1]]

            if isinstance(values, list):
                values = ", ".join(values)
        # display.v(f"= result: {key} {values}")
        return key, values

    def valid_list_data(self, data, valid_entries):
        """
        """
        result = []

        if isinstance(data, list):
            data.sort()
            valid_entries.sort()
            result = list(set(data).intersection(valid_entries))
            result.sort()
        # display.v(f"=result: {result}")
        return result
