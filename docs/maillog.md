

```yaml
postfix_maillog:
  file: ""
  file_compressor: gzip
  file_prefixes:
    - /var
    - /dev/stdout
  file_rotate_suffix: "%Y%m%d-%H%M%S"
```
