
# `main.cf`

## smtp

```yaml
postfix_smtp:
  address_preference: ""                            # any
  address_verify_target: ""                         # rcpt
  always_send_ehlo: ""                              # yes
  balance_inet_protocols: ""                        # yes
  bind_address: ""                                  #
  bind_address6: ""                                 #
  body_checks: ""                                   #
  cname_overrides_servername: ""                    # no
  connect_timeout: ""                               # 30s
  connection:
    cache:
      destinations: ""                              #
      on_demand: ""                                 # yes
      time_limit: ""                                # 2s
    reuse:
      count_limit: ""                               # 0
      time_limit: ""                                # 300s
  data:
    done_timeout: ""                                # 600s
    init_timeout: ""                                # 120s
    xfer_timeout: ""                                # 180s
  defer_if_no_mx_address_found: ""                  # no
  delivery:
    slot:
      cost: ""                                      # $default_delivery_slot_cost
      discount: ""                                  # $default_delivery_slot_discount
      loan: ""                                      # $default_delivery_slot_loan
    status_filter: ""                               # $default_delivery_status_filter
  destination:
    concurrency:
      failed_cohort_limit: ""                       # $default_destination_concurrency_failed_cohort_limit
      limit: ""                                     # $default_destination_concurrency_limit
      negative_feedback: ""                         # $default_destination_concurrency_negative_feedback
      positive_feedback: ""                         # $default_destination_concurrency_positive_feedback
    rate_delay: ""                                  # $default_destination_rate_delay
    recipient_limit: ""                             # $default_destination_recipient_limit
  discard:
    ehlo:
      keyword_address_maps: ""
      keywords: ""
  dns:
    reply_filter: []                                # []
    resolver_options: []                            # [res_defnames, res_dnsrch]
    support_level: ""                               # "disabled", "enabled", "dnssec"
  enforce_tls: ""                                   # false
  extra_recipient_limit: ""                         # $default_extra_recipient_limit
  fallback_relay: ""                                # $fallback_relay
  generic_maps: []                                  # [hash:/etc/postfix/generic]
  header_checks: []                                 # [hash:/etc/postfix/header_checks]
  helo:
    name: ""                                        # $myhostname
    timeout: ""                                     # 300s
  host_lookup: []                                   # dns
  initial_destination_concurrency: ""               # $initial_destination_concurrency
  line_length_limit: ""                             # 998
  mail_timeout: ""                                  # 300s
  mime_header_checks: []
  minimum_delivery_slots: ""                        # $default_minimum_delivery_slots
  mx:
    address_limit: ""                               # 5
    session_limit: ""                               # 2
  nested_header_checks: []
  never_send_ehlo: ""                               # no
  per_record_deadline: ""                           # no
  pix:
    workaround:
      delay_time: ""                                # 10s
      maps: []
      threshold_time: ""                            # 500s
    workarounds: []                                 # [disable_esmtp,delay_dotcrlf]
  quit_timeout: ""                                  # 300s
  quote_rfc821_envelope: ""                         # yes
  randomize_addresses: ""                           # yes
  rcpt_timeout: ""                                  # 300s
  recipient:
    limit: ""                                       # $default_recipient_limit
    refill:
      delay: ""                                     # $default_recipient_refill_delay
      limit: ""                                     # $default_recipient_refill_limit
  reply_filter: []
  rset_timeout: ""                                  # 20s
  sasl:
    auth:
      cache:
        name: ""
        time: ""                                    # 90d
      enable: ""                                    # true
      soft_bounce: ""                               # false
      # TODO - https://github.com/bodsch/ansible-postfix/issues/21
      authentication: {}
    mechanism_filter: []                            # [plain, login] / [!gssapi, !login, static:rest] / [/etc/postfix/smtp_mechs]
    password_maps: ""                               # hash:/etc/postfix/maps.d/sasl_passwd
    path: ""
    security_options: []                            # [noanonymous]
    tls:
      security_options: []                          # [noanonymous]
      verified_security_options: []                 # [$smtp_sasl_tls_security_options]
    type: ""                                        # cyrus
  send:
    dummy_mail_auth: ""                             # no
    xforward_command: ""                            # no
  sender_dependent_authentication: ""               # yes
  skip:
    5xx_greeting: ""                                # yes
    quit_response: ""                               # yes
  starttls_timeout: ""                              # 300s
  tcp_port: ""                                      # smtp
  tls:
    ca_file: ""
    ca_path: ""
    block_early_mail_reply: ""                      # no
    cert_file: ""
    chain_files: []
    ciphers: ""                                     # medium
    connection_reuse: ""                            # no
    dane_insecure_mx_policy: ""                     # !unsafe "${{$smtp_tls_security_level} == {dane} ? {dane} : {may}}"
    dcert_file: ""
    dkey_file: ""                                   # "$smtp_tls_dcert_file"
    eccert_file: ""
    eckey_file: ""                                  # "$smtp_tls_eccert_file"
    enforce_peername: ""                            # yes
    exclude_ciphers: ""
    fingerprint:
      cert_match: []
      digest: ""                                    # md5
    force_insecure_host_tlsa_lookup: ""             # no
    key_file: ""                                    # "$smtp_tls_cert_file"
    loglevel: ""                                    # 1
    mandatory:
      ciphers: ""                                   # medium
      exclude_ciphers: []
      protocols: []                                 # []
    note_starttls_offer: ""                         # yes
    per_site: []
    policy_maps: []
    protocols: []
    scert_verifydepth: ""                           # 9
    secure_cert_match: []                           # [nexthop, dot-nexthop]
    security_level: ""                              # encrypt
    servername: ""
    session_cache:
      database: ""                                  # "btree:${data_directory}/smtp_scache"
      timeout: ""                                   # 3600s
    trust_anchor_file: ""
    verify_cert_match: ""                           # hostname
    wrappermode: ""                                 # true
  transport_rate_delay: ""                          # $default_transport_rate_delay
  use_tls: ""                                       # {{ postfix_relay.use_tls | bool }}"
  xforward_timeout: ""                              # 300s
  #
  generic_maps_database_type: "hash"
```
