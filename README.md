
# Ansible Role:  `postfix`

Ansible role to install and configure postfix on various linux systems.

[upstream documentation ](http://www.postfix.org/postconf.5.html)

## Requirements & Dependencies


### Operating systems

Tested on

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

#### smtpd

```yaml
postfix_smtpd:
  use_tls: true
  client_restrictions: []
  helo_restrictions: []
  sender_restrictions: []
  recipient_restrictions: []
  relay_restrictions:
    - permit_mynetworks
    - permit_sasl_authenticated
    - defer_unauth_destination
  data_restrictions:
    - reject_unauth_pipelining
    - permit
  tls:
    auth_only: true
    cert_file: "/etc/ssl/certs/ssl-cert-snakeoil.pem"
    key_file: "/etc/ssl/private/ssl-cert-snakeoil.key"
    dh1024_param_file: ""
    eecdh_grade: auto
    exclude_ciphers:
      - ECDHE-RSA-RC4-SHA
      - RC4
      - aNULL
      - DES-CBC3-SHA
      - ECDHE-RSA-DES-CBC3-SHA
      - EDH-RSA-DES-CBC3-SHA
    loglevel: 1
    mandatory_ciphers: high
    mandatory_protocols:
      - "!SSLv2"
      - "!SSLv3"
      - "!TLSv1"
      - "!TLSv1.1"
    protocols:
      - "!SSLv2"
      - "!SSLv3"
    received_header: true
    security_level: may
  sasl:
    auth_enable: false
    authenticated_header: true
    path: "" # inet:dovecot:10001
    type: "" # dovecot
```

#### smtp

```yaml
postfix_smtp:
  use_tls: "{{ postfix_relay.use_tls | bool }}"
  generic_maps_file: "hash:{{ postfix_maps_directory }}/generic"
  header_checks_file: "hash:{{ postfix_maps_directory }}/header_checks"
  generic_maps: []
  dns_support_level: ""
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
    cafile: ""
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

#### alias

```yaml
postfix_alias:
  maps_file: "hash:{{ postfix_aliases_file }}"
  database_file: "hash:{{ postfix_aliases_file }}"
```

#### sender

```yaml
postfix_sender:
  based_routing: false
  bcc_maps: []
  canonical_classes: []
  canonical_maps: []
  canonical_maps_file: "hash:{{ postfix_maps_directory }}/sender_canonical_maps"
  dependent_default_transport_maps: []
  dependent_relayhost_maps: []
  dependent_relayhost_maps_file: "hash:{{ postfix_maps_directory }}/sender_dependent_relayhost_maps"
```

#### recipient

```yaml
postfix_recipient:
  canonical_maps_file: "hash:{{ postfix_maps_directory }}/recipient_canonical_maps"
  canonical_maps: []
```

#### transport

```yaml
postfix_transport:
  maps_files:
    - "hash:{{ postfix_maps_directory }}/transport_maps"
  transport_maps: []
```

#### inet
  
[upstream doku](http://www.postfix.org/postconf.5.html#inet_interfaces)
  
```yaml
postfix_inet:
  interfaces:
    - loopback-only
  protocols:
    - ipv4
```

#### relay

```yaml
postfix_relay:
  use_tls: false
  mxlookup: false
  host: ''
  port: 587
  domains_file: ''
  recipient_maps_file: ''
```

#### header

```yaml
postfix_header:
  checks: []
  checks_database_type: regexp
```

#### virtual

```yaml
postfix_virtual:
  alias_maps_files:
    - "hash:{{ postfix_maps_directory }}/virtual"
  aliases: []
```

#### postscreen

```yaml
postfix_postscreen:
  access_list:
    - permit_mynetworks
    - cidr:/opt/postfix/conf/custom_postscreen_whitelist.cidr
    - cidr:/opt/postfix/conf/postscreen_access.cidr
    - tcp:127.0.0.1:10027
  bare_newline_enable: false
  blacklist_action: enforce
  cache_cleanup_interval: 2h
  cache_map: "proxy:btree:$data_directory/postscreen_cache"
  discard_ehlo_keywords: ""
  dnsbl_action: "ignore"
  dnsbl_sites: []
  dnsbl_threshold: 6
  dnsbl_ttl: 5m
  greet_action: ignore
  greet_banner: "$smtpd_banner"
  greet_ttl: 2d
  greet_wait: "${stress?2}${stress:6}s"
  non_smtp_command_enable: false
  pipelining_enable: false
```

#### proxy

```yaml
postfix_proxy:
  read_maps: []
  write_maps: []
  interfaces: ""
```

### master.cf

[upstream doku](http://www.postfix.org/master.5.html)

|         | type     |       |                |                                    |
| :----   | :----    | :---- | :----          | :----                              |
| service | *string* / *int* | `smtp` / `589` | service name oder port             |
| type    | *string*         | `inet`         | service type                       |
| private | *bool*           | `false`        |                                    |
| unpriv  | *bool*           | `false`        |                                    |
| chroot  | *bool*           | `false`        |                                    |
| wakeup  | *int*            | `60`           |                                    |
| maxproc | *int*            | `100`          |                                    |
| command | *string*         | `postscreen`   | postfix command                    |
| args    | *list*           | ` []`          | liste von argumenten für `command` |

```yaml
postfix_master:
  smtp:
    type: inet
    private: false
    chroot: false
    command: smtpd
    args: []
  # smtp      inet  n       -       n       -       1       postscreen
  smtp:
    enabled: false
    type: inet
    private: false
    chroot: false
    maxproc: 1
    command: postscreen
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
