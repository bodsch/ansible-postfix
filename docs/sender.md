
# `main.cf` 

## sender

```yaml
postfix_sender:
  based_routing: false
  bcc_maps: []
  canonical_classes: []
  canonical_maps: []
  dependent_default_transport_maps: []
  dependent_relayhost_maps: []
  #
  canonical_maps_database_type: "hash"
  canonical_maps_file: "hash:{{ postfix_maps_directory }}/sender_canonical_maps"
  dependent_relayhost_maps_file: "" # hash:{{ postfix_maps_directory }}/sender_dependent_relayhost_maps"

```

