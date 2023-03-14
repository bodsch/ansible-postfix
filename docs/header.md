
# `main.cf` 

## header

Restricted `header_checks` tables for the Postfix SMTP client.  
These tables are searched while mail is being delivered.

Actions that change the delivery time or destination are not available. 

`smtp_header_checks`

create file `/etc/postfix/maps.d/header_checks`

```yaml
postfix_header:
  checks: []
  checks_database_type: regexp
```

### Define own `header_checks`

Optional lookup tables for content inspection of primary non-MIME message headers, 
as specified in the [header_checks(5)](https://www.postfix.org/header_checks.5.html) manual page. 

> **Only valid action commands are supported!**

```
postfix_header:
  checks:
    - pattern: /^Message-ID:.*<!&!/
      action: DUNNO
    - pattern: /^Message-ID:.*@(porcupine\.org)/"
      action: REJECT
      text: "forged domain name in Message-ID: header: $1"
```
