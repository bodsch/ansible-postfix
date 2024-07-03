
# `main.cf` 

## recipient

```yaml
postfix_recipient:
  bcc_maps: ""
  canonical_classes: ""         # envelope_recipient
  canonical_maps: []
  delimiter: ""                 # +
  canonical_maps_database_type: "lmdb"
  canonical_maps_files:
    - "lmdb:{{ postfix_maps_directory }}/recipient_canonical_maps"
```

### canonical_maps

```yaml
postfix_recipient:
  canonical_maps:
    - sender: root@your-private.lan
      rewrite: webmaster@yourdomain.com
```
