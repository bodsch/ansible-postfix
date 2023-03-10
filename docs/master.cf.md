
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
