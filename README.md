
# Ansible Role:  `postfix`

Ansible role to install and configure postfix on various linux systems.

[upstream documentation ](http://www.postfix.org/postconf.5.html)


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-postfix/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-postfix)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-postfix)][releases]

[ci]: https://github.com/bodsch/ansible-postfix/actions
[issues]: https://github.com/bodsch/ansible-postfix/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-postfix/releases


## Requirements & Dependencies


### Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 9 / 10 / 11
    - Ubuntu 20.10

## configuration

### main.cf

```yaml
postfix_smtpd_banner: '$myhostname ESMTP $mail_name'
postfix_hostname: "{{ ansible_fqdn }}"
postfix_mailname: "{{ ansible_fqdn }}"

postfix_myorigin: "{{ postfix_mailname_file }}"
postfix_delay_warning_time: ''
postfix_compatibility_level: '3'

# http://www.postfix.org/DATABASE_README.html#types
postfix_default_database_type: hash
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

postfix_mailbox_size_limit: 0
postfix_message_size_limit: 10240000
```

- [alias](docs/alias.md)
- [header](docs/header.md)
- [inet](docs/inet.md)
- [postscreen](docs/postscreen.md)
- [proxy](docs/proxy.md)
- [recipient](docs/recipient.md)
- [relay](docs/relay.md)
- [sender](docs/sender.md)
- [smtpd](docs/smtpd.md)
- [smtp](docs/smtp.md)
- [tls](docs/tls.md)
- [transport](docs/transport.md)
- [virtual](docs/virtual.md)


### master.cf

To manage the `master.cf` via the role, this feature must be explicitly **enabled**:

```yaml
postfix_handle_mastercf: true
```

[upstream doku](http://www.postfix.org/master.5.html)

|           | type             |                |                                    |
| :----     | :----            | :----          | :----                              |
| `service` | *string* / *int* | `smtp` / `589` | service name oder port             |
| `comment` | *string*         | `-`            | comment                            |
| `enable`  | *bool*           | `true`         | enable or disable service          |
| `type`    | *string*         | `inet`         | service type                       |
| `private` | *bool*           | `false`        |                                    |
| `unpriv`  | *bool*           | `false`        |                                    |
| `chroot`  | *bool*           | `false`        |                                    |
| `wakeup`  | *int*            | `60`           |                                    |
| `maxproc` | *int*            | `100`          |                                    |
| `command` | *string*         | `postscreen`   | postfix command                    |
| `args`    | *list*           | `[]`           | liste von argumenten für `command` |

```yaml
postfix_master:
  # service   type  private unpriv  chroot  wakeup  maxproc command + args
  # smtp      inet  n       -       n       -       1       postscreen
  smtp:
    comment: >
       standard smtp service
    enabled: false
    type: inet
    private: false
    unpriv: ''
    chroot: false
    wakeup: ''
    maxproc: 1
    command: postscreen
    args: []
```

for more examples, see [vars/main.yml](vars/mail.yml)

For multiple services that only require different parameters, e.g. use a different `type` or `command`,
the servicename can be **overwritten** via `service`:

```yaml
postfix_master:
  smtp:
    comment: >
       standard smtp service
    type: inet
    private: false
    chroot: false
    command: smtpd
    args: []
  # smtp      inet  n       -       n       -       1       postscreen
  smtp_with_postscreen:
    comment: >
      smtp service with postscreen backend.
      currently disabled
    service: smtp
    enabled: false
    type: inet
    private: false
    chroot: false
    maxproc: 1
    command: postscreen
```

This Part generates following lines in the `master.cf`:

```bash
# standard smtp service
smtp            inet              n        -        n        -        -           smtpd
# smtp service with postscreen backend.  currently disabled
# smtp            inet              n        -        n        -        1           postscreen

```


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://gitlab.com/bodsch/ansible-postfix/-/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
