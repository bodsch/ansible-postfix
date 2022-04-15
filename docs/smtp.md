
# `main.cf`

## smtp

```yaml
postfix_smtp:
  use_tls: "{{ postfix_relay.use_tls | bool }}"
  generic_maps_file: ""
  header_checks_file: ""
  generic_maps: []
  generic_maps_database_type: "hash"
  dns_support_level: ""
  dependent_authentication: true
  sasl:
    auth_enable: true
    user: "postmaster@localhost"
    password: ""
    password_maps_file: "hash:{{ postfix_maps_directory }}/sasl_passwd"
    security_options: noanonymous
    tls_security_options: noanonymous
    mechanism_filter: ""
    auth_soft_bounce: false
  tls:
    security_level: encrypt
    note_starttls_offer: true
    wrappermode: true
    ca_file: ""
    cert_file: ""
    key_file: ""
    loglevel: 1
    mandatory_protocols:
      - "!SSLv2"
      - "!SSLv3"
      - "!TLSv1"
      - "!TLSv1.1"
    protocols:
      - "!SSLv2"
      - "!SSLv3"
    policy_maps_file: ""
```
