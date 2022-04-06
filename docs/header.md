
# `main.cf` 

## header

Restricted header_checks tables for the Postfix SMTP client.
These tables are searched while mail is being delivered.
Actions that change the delivery time or destination are not available. 

`smtp_header_checks`

create file `/etc/postfix/header_checks`

```yaml
postfix_header:
  checks: []
  checks_file: ""
  checks_database_type: regexp
```
