
# `main.cf`

## smtpd

```yaml
postfix_smtpd:
  use_tls: true
  client_restrictions: []
  helo_restrictions: []
  sender_restrictions: []
  sender_login_maps: []
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
    chain_files: []
    dh1024_param_file: ""
    eecdh_grade: auto
    cipherlist: []
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
  milters: ""
  proxy_timeout: 600s
``` 
