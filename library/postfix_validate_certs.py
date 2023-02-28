#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2022-2023, Bodo Schulz <bodo@boone-schulz.de>


from __future__ import absolute_import, division, print_function
import os

from ansible.module_utils.basic import AnsibleModule


class PostfixValidateCerts(object):
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
        res = dict(
            failed = False,
            msg = "module init"
        )

        if isinstance(self.config, dict):
            """
            """
            res = self.validate(self.config)

        # self.module.log(f"  - res: {res}")

        return res

    def validate(self, config):
        """
        """
        res = dict()

        cert_file = config.get('cert_file', None)
        key_file = config.get('key_file', None)
        ca_file = config.get('ca_file', None)
        chain_files = config.get('chain_files', [])

        # self.module.log(f"cert_file  : {cert_file}")
        # self.module.log(f"key_file   : {key_file}")
        # self.module.log(f"ca_file    : {ca_file}")
        # self.module.log(f"chain_files: {chain_files}")

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

    postfix = PostfixValidateCerts(module)
    result = postfix.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
