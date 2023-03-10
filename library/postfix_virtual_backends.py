#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2023, Bodo Schulz <bodo@boone-schulz.de>

# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os
import hashlib
import json

from ansible.module_utils.basic import AnsibleModule

TPL_BACKEND = """# generated by ansible
user     = {{ item.username }}
password = {{ item.password }}
hosts    = {{ item.hosts }}
dbname   = {{ item.dbname }}

query    =
  {{ item.query | indent(2, first=False, blank=False) }}
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
        if isinstance(plaintext, dict):
            _data = json.dumps(plaintext, sort_keys=True)
        else:
            _data = plaintext.copy()

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

        if isinstance(data, dict):
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


class PostfixVirtualBackends(object):
    """
    """

    def __init__(self, module):
        """
        """
        self.module = module

        self.dest = module.params.get("dest")
        self.backends = module.params.get("backends")
        self.cache_directory = "/var/cache/ansible/postfix"

    def run(self):
        """
        """
        _changed = False
        _failed = True
        _msg = "module init"

        self.checksum = Checksum(self.module)

        result_state = []

        self.__create_directory(self.cache_directory)
        checksum_file = os.path.join(self.cache_directory, "backends")

        changed, checksum, old_checksum = self.checksum.validate(
            checksum_file=checksum_file,
            data=self.backends
        )

        if not changed:
            return dict(
                changed = False,
                msg = "The backend configuration has not been changed."
            )

        for backend_type, backend_def in self.backends.items():
            res = {}
            self.__create_directory(os.path.join(self.dest, backend_type))

            for backend_data in backend_def:
                file_name = backend_data.get('name', None)

                if not file_name:
                    # password param should not be logged!
                    backend_data["password"] = "******"

                    # valid = False
                    msg = f"ERROR: missing 'name' for this broken backend definition: {backend_data}"

                    res["general"] = dict(
                        failed=True,
                        msg=msg
                    )

                else:
                    res[file_name] = dict()

                    valid, _msg = self._validate_backend(backend_data)

                    if valid:
                        _failed, _changed, _msg = self._write_template(os.path.join(self.dest, backend_type, file_name), backend_data)

                        res[file_name] = dict(
                            failed=_failed,
                            changed=_changed,
                            msg=_msg
                        )

                    else:
                        res[file_name] = dict(
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

    def _validate_backend(self, backend_data):
        """
        """
        valid = False
        msg = "alles ist um seife"

        error_msg = []

        # self.module.log(f"    {backend}")
        file_name = backend_data.get('name', None)
        db_username = backend_data.get('username', None)
        db_password = backend_data.get('password', None)
        db_hosts = backend_data.get('hosts', None)
        db_name = backend_data.get('dbname', None)
        db_query = backend_data.get('query', None)

        if not file_name:
            error_msg.append("name")
            # password param schould not be logged!
            backend_data["password"] = "******"
            msg = f"ERROR: broken backend definition: {backend_data}"

        else:
            if not db_username:
                error_msg.append("username")
            if not db_password:
                error_msg.append("password")
            if not db_hosts:
                error_msg.append("hosts")
            if not db_name:
                error_msg.append("dbname")
            if not db_query:
                error_msg.append("query")

            if len(error_msg) > 0:
                msg = f"The variables for '{file_name}' have not been defined: "
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

        checksum_file = os.path.join(self.cache_directory, f"{os.path.basename(file_name)}.checksum")

        changed, checksum, old_checksum = self.checksum.validate(
            checksum_file=checksum_file,
            data=data
        )

        if not changed:
            return False, False, "The configuration file has not been changed."

        from jinja2 import Template

        tm = Template(TPL_BACKEND)
        d = tm.render(item=data)

        with open(file_name, "w") as f:
            f.write(d)

        self.checksum.write_checksum(
            checksum_file=checksum_file,
            checksum=checksum
        )

        return False, True, "The configuration file was written successfully."

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

# ===========================================
# Module execution.


def main():
    """
    """
    args = dict(
        backends = dict(
            required=True,
            type='dict'
        ),
        dest = dict(
            required=True,
            type='str'
        )
    )

    module = AnsibleModule(
        argument_spec=args,
        supports_check_mode=True,
    )

    p = PostfixVirtualBackends(module)
    result = p.run()

    module.log(msg=f"= result: {result}")
    module.exit_json(**result)


if __name__ == '__main__':
    main()
