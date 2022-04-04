
# `main.cf` 

## transport

```yaml
postfix_transport:
  maps_files:
    - "hash:{{ postfix_maps_directory }}/transport_maps"
  transport_maps: []
```
