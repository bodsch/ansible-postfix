
# `main.cf` 

## tls

### defaults

```yaml
postfix_tls:
  protocols:
    smtp: []
    lmtp: []
    smtpd: []
  preempt_cipherlist: true
  server_sni_maps: "" # hash:/opt/postfix/conf/sni.map"
  ssl_options: []
```

### example

```yaml
postfix_tls:
  protocols:
    smtp:
      - "!SSLv2"
      - "!SSLv3"
      - "!TLSv1"
      - "!TLSv1.1"
    lmtp:
      - "!SSLv2"
      - "!SSLv3"
      - "!TLSv1"
      - "!TLSv1.1"
    smtpd:
      - "!SSLv2"
      - "!SSLv3"
      - "!TLSv1"
      - "!TLSv1.1"
  ssl_options:
    - NO_COMPRESSION
    - NO_RENEGOTIATION
```
