
# `main.cf`

## inet

[upstream doku](http://www.postfix.org/postconf.5.html#inet_interfaces)

```yaml
postfix_inet:
  interfaces:
    - loopback-only
  protocols:
    - ipv4
```
