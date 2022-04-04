
# `main.cf` 

## recipient

```yaml
postfix_recipient:
  canonical_maps_file: "hash:{{ postfix_maps_directory }}/recipient_canonical_maps"
  canonical_maps: []
```

