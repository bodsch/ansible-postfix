
# `main.cf`

## inet

[upstream doku](http://www.postfix.org/postconf.5.html#inet_interfaces)

```yaml
postfix_inet:
  # 'all' or a list of interfaces
  # http://www.postfix.org/postconf.5.html#inet_interfaces
  interfaces:
    - loopback-only
  # 'all' or a list of valid protocols like 'ipv4'
  protocols:
    - ipv4
```
