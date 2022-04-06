
# `main.cf` 

## postscreen

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

