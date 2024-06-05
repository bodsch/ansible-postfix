
# `main.cf` 

## transport

```yaml
postfix_transport:
  maps: []
  #   - "lmdb:{{ postfix_maps_directory }}/transport_maps"
  retry_time: ""                                    # 60s
  # used by handlers
  maps_database_type: "lmdb"
```
