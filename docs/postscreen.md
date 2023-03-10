
# `main.cf` 

## postscreen

```yaml
postfix_postscreen:
  enable: false
  access_list:
    - permit_mynetworks
    # - cidr:/opt/postfix/conf/custom_postscreen_whitelist.cidr
    # - cidr:/opt/postfix/conf/postscreen_access.cidr
    # - tcp:127.0.0.1:10027
  bare_newline_action: ignore
  bare_newline_enable: false
  bare_newline_ttl: 30d
  # renamed to postscreen_denylist_action in Postfix 3.6.
  #  - ignore (default)
  #  - enforce
  #  - drop
  blacklist_action: ignore
  cache_cleanup_interval: 2h
  cache_map: "proxy:btree:$data_directory/postscreen_cache"
  cache_retention_time: 7d
  client_connection_count_limit: $smtpd_client_connection_count_limit
  command_count_limit: 20
  command_filter: ""
  command_time_limit: ${stress?{10}:{300}}s
  # Available as postscreen_blacklist_action in Postfix 2.8 - 3.5.
  denylist_action: ignore
  disable_vrfy_command: ""
  discard_ehlo_keyword_address_maps: ""
  discard_ehlo_keywords: ""  # silent-discard, dsn
  dnsbl_action: "ignore"
  dnsbl_max_ttl: ""  # ${postscreen_dnsbl_ttl?{$postscreen_dnsbl_ttl}:{1}}h
  dnsbl_min_ttl: ""  # 60s
  dnsbl_reply_map: ""
  dnsbl_sites: []
  dnsbl_threshold: 6
  dnsbl_timeout: 10s
  dnsbl_whitelist_threshold: 0
  dnsbl_ttl: 5m
  enforce_tls: ""  # $smtpd_enforce_tls
  expansion_filter: ""  # $smtpd_expansion_filter
  forbidden_commands: ""  # $smtpd_forbidden_commands
  greet_action: ignore
  greet_banner: ""
  greet_ttl: ""       # 1d
  greet_wait: ""      # ${stress?2}${stress:6}s
  helo_required: ""   # $smtpd_helo_required
  non_smtp_command_action: ""   # drop
  non_smtp_command_enable: ""   # false
  non_smtp_command_ttl: ""      # 30d
  pipelining_action: ""         #  enforce
  pipelining_enable: ""         #  false
  pipelining_ttl: ""            #  30d
  post_queue_limit: $default_process_limit
  pre_queue_limit: $default_process_limit
  reject_footer: $smtpd_reject_footer
  reject_footer_maps: $smtpd_reject_footer_maps
  tls_security_level: $smtpd_tls_security_level
  upstream_proxy_protocol: ""
  upstream_proxy_timeout: 5s
  use_tls: $smtpd_use_tls
  watchdog_timeout: 10s
  whitelist_interfaces: static:all
```

