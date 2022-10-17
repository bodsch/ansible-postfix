#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule


class PostfixCheck(object):
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self._postfix = module.get_bin_path('postfix', True)
        self.verbose = module.params.get("verbose")

    def run(self):
        """
          runner
        """
        result = dict(
            rc=127,
            failed=True,
            changed=False,
        )

        args = []
        args.append(self._postfix)

        if self.verbose:
            args.append("-v")

        args.append("check")

        rc, out, err = self._exec(args)

        result['rc'] = rc

        if rc == 0:
            result['failed'] = False
            result['changed'] = True
            result['msg'] = out
        else:
            result['failed'] = True
            result['changed'] = False
            result['msg'] = err

        return result

    def _exec(self, cmd):
        """
        """
        rc, out, err = self.module.run_command(cmd, check_rc=True)

        return rc, out, err


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            verbose=dict(
                required=False,
            )
        ),
        supports_check_mode=True,
    )

    postfix = PostfixCheck(module)
    result = postfix.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
