#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os

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

        self.verbose = module.params.get("verbose")
        self.config = module.params.get("config")

    def run(self):
        """
          runner
        """
        res = {}

        if isinstance(self.config, dict):
            """
            """
            cert_file = self.config.get('cert_file', None)
            key_file = self.config.get('key_file', None)
            ca_file = self.config.get('ca_file', None)
            # TODO
            # chain_files = self.config.get('chain_files', [])

            if cert_file:
                if not os.path.exists(cert_file):
                    res['cert'] = dict(
                        failed = True,
                        msg = f"file {cert_file} does not exists."
                    )

            if key_file:
                if not os.path.exists(key_file):
                    res['key'] = dict(
                        failed = True,
                        msg = f"file {key_file} does not exists."
                    )

            if ca_file:
                if not os.path.exists(ca_file):
                    res['ca'] = dict(
                        failed = True,
                        msg = f"file {ca_file} does not exists."
                    )

            pass

        result_failed  = {k: v for k, v in res.items() if v.get('failed')}

        # find all failed and define our variable
        failed = (len(result_failed) > 0)

        final_result = dict(
            failed = failed
        )

        if failed:
            final_result.update({
                "result_failed": result_failed
            })

        return final_result


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            verbose=dict(
                required=False,
            ),
            config=dict(
                type=dict,
                required= True
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
