
# `main.cf` 

## tls

```yaml
postfix_defaults_tls:
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
  preempt_cipherlist: true
  server_sni_maps: "hash:/opt/postfix/conf/sni.map"
  ssl_options:
    - NO_COMPRESSION
    - NO_RENEGOTIATION
```
