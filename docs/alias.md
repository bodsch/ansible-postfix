
# `main.cf`

`alias_database`
`alias_maps`

## alias

The alias databases for local delivery that are updated with `newaliases` or with `sendmail -bi`.

```yaml
postfix_aliases_file: /etc/aliases

postfix_alias:
  maps_file: "hash:{{ postfix_aliases_file }}"
  database_file: "hash:{{ postfix_aliases_file }}"
```
