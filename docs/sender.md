
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
  canonical_maps_database_type: "lmdb"
  canonical_maps_files: 
    - "lmdb:{{ postfix_maps_directory }}/sender_canonical_maps"
  dependent_relayhost_maps_files: [] # lmdb:{{ postfix_maps_directory }}/sender_dependent_relayhost_maps"
```

### canonical_maps

```yaml
postfix_sender:

  canonical_maps:
    - sender: '/^((root|dbsupport|helpdesk).*)your-private[.]lan$/'
      rewrite: admin@yourdomain.com
    - sender: root
      rewrite: admin@yourdomain.com
    - sender: root@your-private.lan
      rewrite: admin@yourdomain.com
```

### dependent_relayhost_maps

```yaml
postfix_sender:

  dependent_relayhost_maps:
    - pattern: 'logcheck@yourdomain.org'
      result: 'DUNNO'
    - pattern: 'pflogsumm@yourdomain.org'
      result: 'DUNNO'
    - pattern: '*'
      result: "smtp:{{ ansible_lo['ipv4']['address'] }}:1025"
```
