
# `main.cf`

## smtpd

```yaml
postfix_smtpd:
  authorized:
    verp_clients: ""                                # $authorized_verp_clients
    xclient_hosts: ""
    xforward_hosts: ""
  banner: '$myhostname ESMTP $mail_name'
  client:
    auth_rate_limit: ""                             # 0
    connection:
      count_limit: ""                               # 50
      rate_limit: ""                                # 0
    event_limit_exceptions: ""                      # ${smtpd_client_connection_limit_exceptions:$mynetworks}
    message_rate_limit: ""                          # 0
    new_tls_session_rate_limit: ""                  # 0
    port_logging: ""                                # no
    recipient_rate_limit: ""                        # 0
    # https://www.postfix.org/postconf.5.html#smtpd_client_restrictions
    restrictions: []
  command_filter: []
  data_restrictions: []                             # [reject_unauth_pipelining, permit]
  delay:
    open_until_valid_rcpt: ""                       # yes
    reject: ""                                      # yes
  discard:
    ehlo:
      keyword_address_maps: []
      keywords: []
  dns_reply_filter: []
  end_of_data_restrictions: []
  enforce_tls: ""                                   # no
  error_sleep_time: ""                              # 10s
  etrn_restrictions: []
  expansion_filter: ""                              # !unsafe \t\40!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~
  forbidden_commands: []                            # CONNECT GET POST
  hard_error_limit: ""                              # ${stress?1}${stress:5}
  helo:
    required: ""                                    # yes
    restrictions: []
  history_flush_threshold: ""                       # 100
  junk_command_limit: ""                            # ${stress?{1}:{100}}
  log_access_permit_actions: []
  milter_maps: []
  milters: []
  noop_commands: []
  null_access_lookup_key: ""                        # <>
  peername_lookup: ""                               # yes
  per_record_deadline: ""                           # ${stress?{yes}:{no}}
  policy:
    service:
      default_action: ""                            # "451 4.3.5 Server configuration problem"
      max_idle: ""                                  # 300s
      max_ttl: ""                                   # 1000s
      policy_context: []
      request_limit: ""                             # 0
      retry_delay: ""                               # 1s
      timeout: ""                                   # 100s
      try_limit: ""                                 # 2
  proxy:
    ehlo: ""                                        # $myhostname
    filter: ""
    options: []
    timeout: ""                                     # 100s
  recipient:
    limit: ""                                       # 1000
    overshoot_limit: ""                             # 1000
    restrictions: []                                # [check_recipient_mx_access permit_sasl_authenticated permit_mynetworks reject_invalid_helo_hostname reject_unauth_destination]
  reject:
    footer: |
      \c. For assistance, call 800-555-0101.
      Please provide the following information in your problem report:
      time ($localtime), client ($client_address) and server
      ($server_name).
    footer_maps: []
    unlisted:
      recipient: ""                                 # yes
      sender: ""                                    # no
  relay_restrictions: []                            # permit_mynetworks permit_sasl_authenticated defer_unauth_destination reject_unauth_destination
  restriction_classes: []
  sasl:
    auth_enable: ""                                 # no
    authenticated_header: ""                        # no
    exceptions_networks: []                         #
    local_domain: ""                                #
    path: ""                                        # smtpd
    response_limit: ""                              # 12288
    # https://www.postfix.org/postconf.5.html#smtpd_sasl_security_options
    security_options: []                            # [noanonymous]
    service: ""                                     # smtp
    tls_security_options: ""                        # "$smtpd_sasl_security_options"
    type: ""                                        # dovecot, cyrus
  sender:
    login_maps: []
    restrictions: []                                # [reject_authenticated_sender_login_mismatch permit_mynetworks permit_sasl_authenticated reject_unlisted_sender reject_unknown_sender_domain]
  service_name: ""                                  # smtpd
  soft_error_limit: ""                              # 3
  starttls_timeout: ""                              # ${stress?{10}:{300}}s
  timeout: ""                                       # ${stress?{10}:{300}}s
  tls:
    ca_file: ""                                     # "/etc/ssl/private/ssl-ca-snakeoil.cabundle"
    ca_path: ""
    always_issue_session_ids: ""                    # yes
    ask_ccert: ""                                   # no
    auth_only: ""                                   # true
    always_issue_session_ids: ""                    # yes
    cert_file: ""                                   # "/etc/ssl/certs/ssl-cert-snakeoil.pem"
    chain_files: []
    ciphers: ""                                     # medium
    dcert_file: ""
    dh1024_param_file: ""
    dh512_param_file: ""
    dkey_file: ""                                   # $smtpd_tls_dcert_file
    eccert_file: ""
    eckey_file: ""                                  # $smtpd_tls_eccert_file
    eecdh_grade: ""                                 # auto
    exclude_ciphers: []                             # [ECDHE-RSA-RC4-SHA, RC4, aNULL, DES-CBC3-SHA, ..]
    fingerprint_digest: ""                          # md5
    key_file: ""                                    # "/etc/ssl/private/ssl-cert-snakeoil.key"
    loglevel: ""                                    # 1
    mandatory:
      ciphers: ""                                   # high
      exclude_ciphers: []                           # [ECDHE-RSA-RC4-SHA, RC4, aNULL, DES-CBC3-SHA, ..]
      protocols: []                                 # ["!SSLv2", "!SSLv3", "!TLSv1", "!TLSv1.1"]
    protocols: []                                   # ["!SSLv2", "!SSLv3"]
    received_header: ""                             # true
    req_ccert: ""                                   # no
    security_level: ""                              # may
    session_cache:
      database: ""                                  # btree:${data_directory}/smtpd_scache
      timeout: ""                                   # 3600s
    wrappermode: ""                                 # no
  upstream_proxy:
    protocol: ""
    timeout: ""                                     # 5s
  use_tls: ""                                       # yes

``` 
