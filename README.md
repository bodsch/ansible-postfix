
# Ansible Role:  `postfix`

Ansible role to install and configure postfix on various linux systems.

[upstream documentation ](http://www.postfix.org/postconf.5.html)


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-postfix/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-postfix)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-postfix)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-postfix/actions
[issues]: https://github.com/bodsch/ansible-postfix/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-postfix/releases
[quality]: https://galaxy.ansible.com/bodsch/postfix


## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)

```bash
ansible-galaxy collection install bodsch.core
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```

### Operating systems

Tested on

* Arch Linux
* ArtixLinux
* Debian based
    - Debian 10 / 11 / 12
    - Ubuntu 20.04 / 22.04

## configuration

### main.cf

```yaml
postfix_hostname: "{{ ansible_fqdn }}"
postfix_mailname: "{{ ansible_fqdn }}"

postfix_myorigin: "{{ postfix_mailname_file }}"
postfix_delay_warning_time: ''
postfix_compatibility_level: '3'

postfix_aliases: []

postfix_mydestinations:
  - $myhostname
  - "{{ postfix_hostname }}"
  - localdomain
  - localhost
  - localhost.localdomain

postfix_mynetworks:
  - 127.0.0.0/8
  - '[::ffff:127.0.0.0]/104'
  - '[::1]/128'

# /etc/postfix/main.cf
postfix_disable_vrfy_command: true
```

- [alias](docs/alias.md)
- [default](docs/default.md)
- [header](docs/header.md)
- [inet](docs/inet.md)
- [mailbox](docs/mailbox.md)
- [maillog](docs/maillog.md)
- [message](docs/message.md)
- [postscreen](docs/postscreen.md)
- [proxy](docs/proxy.md)
- [queue](docs/queue.md)
- [recipient](docs/recipient.md)
- [reject](docs/reject.md)
- [relay](docs/relay.md)
- [sender](docs/sender.md)
- [smtp](docs/smtp.md)
- [smtpd](docs/smtpd.md)
- [tls](docs/tls.md)
- [transport](docs/transport.md)
- [virtual_backends](docs/virtual_backends.md)
- [virtual](docs/virtual.md)


### master.cf

To manage the `master.cf` via the role, this feature must be explicitly **enabled**:

```yaml
postfix_handle_mastercf: true
```

To learn more about the configuration of `master.cf`, please read the [extended documentation](docs/master.cf.md).

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-postfix/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
