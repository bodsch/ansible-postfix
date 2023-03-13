#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os

from ansible.module_utils.basic import AnsibleModule


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


    def run(self):
        """
          runner
        """
        result = dict(
            rc=127,
            failed=True,
            changed=False,
        )

        for map_data in self.maps:
            """
              - name: sender_canonical_maps
                map_type: "hash"
                map_file: "{{ postfix_maps_directory }}/sender_canonical_maps"
                map_vars: "{{ postfix_sender.canonical_maps | default([]) }}"
                postmap: true
            """



        # if not os.path.exists(self.filename):
        #     return dict(
        #         failed = True,
        #         changed = False,
        #         msg = f"file {self.file_name} does not exists."
        #     )
        #
        # args = []
        # args.append(self._postmap)
        # args.append(f"{self.map_type}:{self.filename}")
        #
        # rc, out, err = self._exec(args)
        #
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
