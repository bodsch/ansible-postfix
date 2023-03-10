
# `main.cf` 

## tls

### defaults

```yaml
postfix_tls:
  append_default_CA: ""                             # false
  daemon_random_bytes: ""                           # 32
  dane_digests: []
  #  - sha512
  #  - sha256
  # http://www.postfix.org/postconf.5.html#tls_disable_workarounds
  disable_workarounds: []
  eecdh_auto_curves: []
  #  - X25519
  #  - X448
  #  - prime256v1
  #  - secp521r1
  #  - secp384r1
  eecdh_strong_curve: ""                            # prime256v1
  eecdh_ultra_curve: ""                             # secp384r1
  export_cipherlist: []
  #  - "aNULL"
  #  - "-aNULL"
  #  - "HIGH"
  #  - "MEDIUM"
  #  - "LOW"
  #  - "EXPORT"
  #  - "+RC4"
  #  - "@STRENGTH"
  fast_shutdown_enable: ""                          #  true
  high_cipherlist: []
  #  - "aNULL"
  #  - "-aNULL"
  #  - "HIGH"
  #  - "@STRENGTH"
  legacy_public_key_fingerprints: ""                # false
  low_cipherlist: ""                                # "aNULL:-aNULL:HIGH:MEDIUM:LOW:+RC4:@STRENGTH"
  medium_cipherlist: ""                             # "aNULL:-aNULL:HIGH:MEDIUM:+RC4:@STRENGTH"
  null_cipherlist: ""                               # "eNULL:!aNULL"
  preempt_cipherlist: ""                            # true
  random_bytes: ""                                  # 32
  random_exchange_name: ""                          # "${data_directory}/prng_exch"
  random_prng_update_period: ""                     # 3600s
  random_reseed_period: ""                          # 3600s
  random_source: ""                                 # dev:/dev/urandom
  server_sni_maps: ""                               # hash:/opt/postfix/conf/sni.map"
  session_ticket_cipher: ""                         # aes-256-cbc
  # http://www.postfix.org/postconf.5.html#tls_ssl_options
  ssl_options: []
  wildcard_matches_multiple_labels: ""              # yes
  tlsmgr_service_name: ""                           # tlsmgr
```

### example

```yaml
postfix_tls:
  ssl_options:
    # http://www.postfix.org/postconf.5.html#tls_ssl_options
    - ENABLE_MIDDLEBOX_COMPAT
    - LEGACY_SERVER_CONNECT
    - NO_TICKET
    - NO_COMPRESSION
    - NO_RENEGOTIATION
    - NO_SESSION_RESUMPTION_ON_RENEGOTIATION
    - PRIORITIZE_CHACHA


```
