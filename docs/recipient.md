
# `main.cf` 

## recipient

```yaml
postfix_recipient:
  bcc_maps: ""
  canonical_classes: ""         # envelope_recipient
  canonical_maps: []
  delimiter: ""                 # +
  canonical_maps_database_type: "hash"
  canonical_maps_files: []      # hash:{{ postfix_maps_directory }}/recipient_canonical_maps"
```

