#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os
import hashlib
import json

from ansible.module_utils.basic import AnsibleModule


TPL_BACKEND = """# generated by ansible

{% for i in item %}
  {%- for key, value in i.items() -%}
{{ "{:<40}".format(key) }}  {{ value }}
  {%- endfor %}
{% endfor %}
"""


class Checksum():
    """
        temporary
        in the future, i will use the bodsch.core collection
    """

    def __init__(self, module):
        self.module = module

    def checksum(self, plaintext):
        """
        """
        if isinstance(plaintext, dict) or isinstance(plaintext, list):
            _data = json.dumps(plaintext, sort_keys=True)
        else:
            _data = plaintext.copy()

        self.module.log(f"'{_data}'")

        _bytes = _data.encode('utf-8')

        _hash = hashlib.sha256(_bytes)
        return _hash.hexdigest()

    def validate(self, checksum_file, data = None):
        """
        """
        old_checksum = None

        if not isinstance(data, str) or not isinstance(data, dict):
            if not data and os.path.exists(checksum_file):
                os.remove(checksum_file)

        if os.path.exists(checksum_file):
            with open(checksum_file, "r") as f:
                old_checksum = f.readlines()[0]

        if isinstance(data, dict) or isinstance(data, list):
            _data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            _data = data
        else:
            _data = data.copy()

        checksum = self.checksum(_data)
        changed = not (old_checksum == checksum)

        return (changed, checksum, old_checksum)

    def write_checksum(self, checksum_file, checksum = None):
        """
        """
        with open(checksum_file, "w") as f:
            f.write(checksum)


class PostfixMaps(object):
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self._postmap = module.get_bin_path('postmap', True)
        self.maps = module.params.get("maps")
        self.cache_directory = "/var/cache/ansible/postfix"

    def run(self):
        """
          runner
        """
        _changed = False
        _failed = True
        _msg = "module init"

        self.__create_directory(self.cache_directory)
        self.__create_directory(os.path.join(self.cache_directory, "maps"))

        self.checksum = Checksum(self.module)

        result_state = []

        checksum_file = os.path.join(self.cache_directory, "maps.checksum")

        changed, checksum, old_checksum = self.checksum.validate(
            checksum_file=checksum_file,
            data=self.maps
        )

        if not changed:
            return dict(
                changed = False,
                msg = "The maps configurations has not been changed."
            )

        for map_data in self.maps:
            """
              - name: sender_canonical_maps
                map_type: "hash"
                map_file: "{{ postfix_maps_directory }}/sender_canonical_maps"
                map_vars: "{{ postfix_sender.canonical_maps | default([]) }}"
                postmap: true
            """
            res = {}

            maps_name = map_data.get("name", None)

            valid, _msg = self._validate_map(map_data)

            if valid:
                file_name = map_data.get("map", {}).get("file", None)
                maps_data = map_data.get("map", {}).get("vars", [])
                maps_type = map_data.get("map", {}).get("type", "hash")
                run_postmap = map_data.get("postmap", True)

                _failed, _changed, _msg = self._write_template(file_name, maps_data)

                if _changed:
                    if run_postmap and maps_type in ["btree", "cdb", "dbm", "fail", "hash", "lmdb", "sdbm"]:
                        args = []
                        args.append(self._postmap)
                        args.append(f"{maps_type}:{file_name}")

                        rc, out, err = self._exec(args)

                        # result['rc'] = rc
                        #
                        # if rc == 0:
                        #     result['failed'] = False
                        #     result['changed'] = True
                        #     result['msg'] = out
                        # else:
                        #     result['failed'] = True
                        #     result['changed'] = False
                        #     result['msg'] = err

                res[maps_name] = dict(
                    failed=_failed,
                    changed=_changed,
                    msg=_msg
                )

            else:
                res[maps_name] = dict(
                    failed=True,
                    msg=_msg
                )

            result_state.append(res)

        # define changed for the running tasks
        # migrate a list of dict into dict
        combined_d = {key: value for d in result_state for key, value in d.items()}
        # find all changed and define our variable
        changed = {k: v for k, v in combined_d.items() if isinstance(v, dict) if v.get('changed')}
        failed = {k: v for k, v in combined_d.items() if isinstance(v, dict) if v.get('failed')}

        _changed = (len(changed) > 0)
        _failed = (len(failed) > 0)

        if not _failed:
            self.checksum.write_checksum(
                checksum_file=checksum_file,
                checksum=checksum
            )

        result = dict(
            changed = _changed,
            failed = _failed,
            result = result_state
        )

        return result

    def _validate_map(self, map_data):
        """
        """
        valid = False
        msg = "alles ist um seife"

        error_msg = []

        maps_name = map_data.get("name", None)
        maps_data = map_data.get("map", {})

        if not maps_name:
            error_msg.append("name")
            msg = f"ERROR: broken maps definition: {map_data}"

        else:
            if len(maps_data) > 0:
                maps_type = maps_data.get("type", "hash")
                maps_file = maps_data.get("file", None)
            else:
                maps_type = "hash"
                maps_file = None

            # self.module.log(f"  - type: '{maps_type}'")
            # self.module.log(f"  - file: '{maps_file}'")
            # self.module.log(f"  - vars: '{maps_vars}'")

            if not maps_type or maps_type not in ["btree", "cdb", "dbm", "fail", "hash", "lmdb", "sdbm"]:
                error_msg.append("type")
            if not maps_file:
                error_msg.append("file")

            if len(error_msg) > 0:
                msg = f"The variables for '{maps_name}' have not been defined: "
                msg += ", ".join(error_msg)
            else:
                valid = True
                msg = None

        return (valid, msg)

    def _write_template(self, file_name, data):
        """
        """
        if isinstance(data, dict):
            """
                sort data
            """
            data = json.dumps(data, sort_keys=True)
            if isinstance(data, str):
                data = json.loads(data)

        checksum_file = os.path.join(self.cache_directory, "maps", f"{os.path.basename(file_name)}.checksum")

        changed, checksum, old_checksum = self.checksum.validate(
            checksum_file=checksum_file,
            data=data
        )

        if not changed:
            return False, False, "The configuration file has not been changed."

        values = self.map_data(data)

        from jinja2 import Template

        tm = Template(TPL_BACKEND)
        d = tm.render(item=values)

        with open(file_name, "w") as f:
            f.write(d)

        self.checksum.write_checksum(
            checksum_file=checksum_file,
            checksum=checksum
        )

        return False, True, "The configuration file was written successfully."

    def map_data(self, data):
        """
        """
        key = None
        values = None
        result = []

        if isinstance(data, list):
            for i in data:
                res = {}
                if isinstance(i, dict):
                    key = i[list(i.keys())[0]]
                    values = i[list(i.keys())[1]]
                    if isinstance(values, list):
                        values = ", ".join(values)
                    res.update({key: values})
                result.append(res)

        return result

    def __create_directory(self, dir):
        """
            temporary
            in the future, i will use the bodsch.core collection
        """
        try:
            os.makedirs(dir, exist_ok=True)
        except FileExistsError:
            pass

        if os.path.isdir(dir):
            return True
        else:
            return False

    def _exec(self, cmd):
        """
        """
        rc, out, err = self.module.run_command(cmd, check_rc=True)

        if rc != 0:
            _out  = out.split("\n")
            _err  = err.split("\n")
            self.module.log(f" - out: '{out}' ({type(out)}) - {len(out)}")
            self.module.log(f" - err: '{err}' ({type(err)}) - {len(err)}")
            self.module.log(f" - out: '{_out}'")
            self.module.log(f" - err: '{_err}'")

        return rc, out, err


# ===========================================
# Module execution.
#


def main():
    """
    """
    args = dict(
        maps=dict(
            required = True,
            type = "list",
        )
    )

    module = AnsibleModule(
        argument_spec=args,
        supports_check_mode=False,
    )

    postmap = PostfixMaps(module)
    result = postmap.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
