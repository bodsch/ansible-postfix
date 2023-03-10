
# `main.cf`

## smtpd

```yaml
postfix_smtpd:
  banner: '$myhostname ESMTP $mail_name'
  use_tls: false
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
    # "/etc/ssl/certs/ssl-cert-snakeoil.pem"
    cert_file: ""
    # "/etc/ssl/private/ssl-cert-snakeoil.key"
    key_file: ""
    # "/etc/ssl/private/ssl-ca-snakeoil.cabundle"
    ca_file: ""
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
    exceptions_networks: []
    local_domain: ""
    mechanism_filter: []
    path: "smtpd" # inet:dovecot:10001
    response_limit: 12288
    #  Specify zero or more of the following:
    # noplaintext
    #     Disallow methods that use plaintext passwords.
    # noactive
    #     Disallow methods subject to active (non-dictionary) attack.
    # nodictionary
    #     Disallow methods subject to passive (dictionary) attack.
    # noanonymous
    #     Disallow methods that allow anonymous authentication.
    # forward_secrecy
    #     Only allow methods that support forward secrecy (Dovecot only).
    # mutual_auth
    #     Only allow methods that provide mutual authentication (not available with Cyrus SASL version 1).
    security_options:
      - noanonymous
    # tls_security_options: "$smtpd_sasl_security_options"
    type: "" # dovecot, cyrus
  milters: ""
  proxy_timeout: ""
``` 
