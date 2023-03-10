
# `main.cf` 

## transport

```yaml
postfix_transport:
  maps: []
  #   - "hash:{{ postfix_maps_directory }}/transport_maps"
  retry_time: ""                                    # 60s
  # used by handlers
  maps_database_type: "hash"
```
