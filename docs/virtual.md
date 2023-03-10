
# `main.cf` 

## virtual

```yaml
postfix_virtual:
  alias_maps_files: []
#    - "hash:{{ postfix_maps_directory }}/virtual"
  aliases: []
  gid_maps: ""            # static:5000
  uid_maps: ""            # static:5000
  mailbox_base: ""        # /var/vmail/
  mailbox_domains: ""     # proxy:mysql:/opt/postfix/conf/sql/mysql_virtual_domains_maps.cf
  mailbox_maps: ""        # proxy:mysql:/opt/postfix/conf/sql/mysql_virtual_mailbox_maps.cf
  minimum_uid: ""         # 104
  transport: ""           # lmtp:inet:dovecot:24
```
