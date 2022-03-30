#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import re

from ansible.module_utils.basic import AnsibleModule


class PostfixPostconf(object):
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self._postconf = module.get_bin_path('postconf', True)
        self.config_name = module.params.get("config_name")

    def run(self):
        """
          runner
        """
        result = dict(
            rc=127,
            failed=True,
            changed=False,
        )

        rc, out, err = self._exec(
            [self._postconf, self.config_name]
        )

        version_string = "unknown"

        # debian:
        #  "icinga2 - The Icinga 2 network monitoring daemon (version: r2.12.3-1)"
        # CentOS Linux:
        #  "icinga2 - The Icinga 2 network monitoring daemon (version: 2.12.3)"
        pattern_1 = re.compile(r"{} = (?P<value_string>.*)".format(self.config_name))

        version = re.search(pattern_1, out)

        if version:
            # version = re.search(pattern_2, version.group('version'))
            value_string = version.group('value_string')

        self.module.log(msg="value: {}".format(value_string))

        result['rc'] = rc

        if rc == 0:
            result['failed'] = False
            result['postconf_value'] = value_string

        return result

    def _exec(self, cmd):
        '''   '''
        self.module.log(msg="cmd: {}".format(cmd))

        rc, out, err = self.module.run_command(cmd, check_rc=True)
        self.module.log(msg="  rc : '{}'".format(rc))
        self.module.log(msg="  out: '{}' ({})".format(out, type(out)))
        self.module.log(msg="  err: '{}'".format(err))
        return rc, out, err


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            config_name=dict(
                required=True,
            )
        ),
        supports_check_mode=True,
    )

    icinga = PostfixPostconf(module)
    result = icinga.run()

    module.log(msg="= result: {}".format(result))

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
