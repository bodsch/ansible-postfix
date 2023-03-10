
# `main.cf` 

## virtual_backends

In order to use a database backend for domain or user administration, it is necessary to create corresponding virtual backends.
This is possible via `postfix_virtual_backends`.

The following parameters must be specified:

- `username`
- `password`
- `hosts`
- `dbname`
- `query`

> **This configuration only allows access to already existing databases!**

## examples

### PostfixAdmin

Here is a minimal example for use via [PostfixAdmin](https://github.com/postfixadmin/postfixadmin):

```yaml
_database_defaults: &DATABASE_DEFAULTS
  username: postfix
  password: fsfasdfasdfasdf
  hosts: database
  dbname: postfix


postfix_virtual_backends:
  mysql:
    - name: alias_maps.cf
      description: ""
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT goto FROM alias WHERE address='%s' AND active = 1

    - name: login_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT
          username AS allowedUser
        FROM mailbox
        WHERE
          username='%s' AND
          active = 1
        UNION
          SELECT goto
          FROM alias
          WHERE
            address='%s' AND
            active = 1;

    - name: domains_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
       SELECT domain FROM domain WHERE domain='%s' AND active = 1

    - name: mailbox_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT maildir FROM mailbox WHERE username='%s' AND active = 1

postfix_smtpd:
  sender_login_maps: proxy:mysql:{{ postfix_virtual_directory }}/mysql/login_maps.cf

postfix_virtual:
  alias_maps_files:
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/alias_maps.cf
  mailbox_domains: proxy:mysql:{{ postfix_virtual_directory }}/mysql/domains_maps.cf
  mailbox_maps: proxy:mysql:{{ postfix_virtual_directory }}/mysql/mailbox_maps.cf
```

### mailcow

The configuration for [mailcow](https://mailcow.email) is much more complex:

```yaml
postfix_virtual_backends:
  mysql:
    - name: mbr_access_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT('FILTER smtp_via_transport_maps:', nexthop) as transport FROM transports
        WHERE '%s' REGEXP destination
          AND active='1'
          AND is_mx_based='1';

    - name: recipient_bcc_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT bcc_dest FROM bcc_maps
        WHERE local_dest='%s'
          AND type='rcpt'
          AND active='1';

    - name: recipient_canonical_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT new_dest FROM recipient_maps
        WHERE old_dest='%s'
          AND active='1';

    - name: relay_ne.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT IF(EXISTS(SELECT address, domain FROM alias
        WHERE address = '%s'
          AND domain IN (
            SELECT domain FROM domain
              WHERE backupmx = '1'
                AND relay_all_recipients = '1'
                AND relay_unknown_only = '1')
        ), 'lmtp:inet:dovecot:24', NULL) AS 'transport'

    - name: relay_recipient_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT DISTINCT
        CASE WHEN '%d' IN (
          SELECT domain FROM domain
            WHERE relay_all_recipients=1
              AND domain='%d'
              AND backupmx=1
        )
        THEN '%s' ELSE (
          SELECT goto FROM alias WHERE address='%s' AND active='1'
        )
        END AS result;

    - name: sasl_access_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT 'REJECT' FROM mailbox WHERE username = '%u' AND JSON_UNQUOTE(JSON_VALUE(attributes, '$.smtp_access')) = '0';

    - name: sasl_passwd_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT_WS(':', username, password) AS auth_data FROM relayhosts
        WHERE id IN (
          SELECT relayhost FROM domain
            WHERE CONCAT('@', domain) = '%s'
            OR '%s' IN (
              SELECT CONCAT('@', alias_domain) FROM alias_domain
            )
        )
        AND username != '';

    - name: sasl_passwd_maps_sender_dependent.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT_WS(':', username, password) AS auth_data FROM relayhosts
        WHERE id IN (
          SELECT COALESCE(
            (SELECT id FROM relayhosts
            LEFT OUTER JOIN domain ON domain.relayhost = relayhosts.id
            WHERE relayhosts.active = '1'
              AND (domain.domain = '%d'
                OR domain.domain IN (
                  SELECT target_domain FROM alias_domain
                  WHERE alias_domain = '%d'
                )
              )
            ),
            (SELECT id FROM relayhosts
            LEFT OUTER JOIN mailbox ON JSON_UNQUOTE(JSON_VALUE(mailbox.attributes, '$.relayhost')) = relayhosts.id
            WHERE relayhosts.active = '1'
              AND (
                mailbox.username IN (
                  SELECT alias.goto from alias
                    JOIN mailbox ON mailbox.username = alias.goto
                      WHERE alias.active = '1'
                        AND alias.address = '%s'
                        AND alias.address NOT LIKE '@%%'
                )
              )
            )
          )
        )
        AND active = '1'
        AND username != '';

    - name: sasl_passwd_maps_transport_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT_WS(':', username, password) AS auth_data FROM transports
        WHERE nexthop = '%s'
        AND active = '1'
        AND username != ''
        LIMIT 1;

    - name: sender_bcc_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT bcc_dest FROM bcc_maps
        WHERE local_dest='%s'
          AND type='sender'
          AND active='1';

    - name: sender_dependent_default_transport_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT GROUP_CONCAT(transport SEPARATOR '') AS transport_maps
        FROM (
          SELECT IF(EXISTS(SELECT 'smtp_type' FROM alias
            LEFT OUTER JOIN mailbox ON mailbox.username = alias.goto
              WHERE (address = '%s'
                OR address IN (
                  SELECT CONCAT('%u', '@', target_domain) FROM alias_domain
                    WHERE alias_domain = '%d'
                )
              )
              AND JSON_UNQUOTE(JSON_VALUE(attributes, '$.tls_enforce_out')) = '1'
              AND mailbox.active = '1'
          ), 'smtp_enforced_tls:', 'smtp:') AS 'transport'
          UNION ALL
          SELECT COALESCE(
            (SELECT hostname FROM relayhosts
            LEFT OUTER JOIN mailbox ON JSON_UNQUOTE(JSON_VALUE(mailbox.attributes, '$.relayhost')) = relayhosts.id
              WHERE relayhosts.active = '1'
                AND (
                  mailbox.username IN (SELECT alias.goto from alias
                    JOIN mailbox ON mailbox.username = alias.goto
                      WHERE alias.active = '1'
                        AND alias.address = '%s'
                        AND alias.address NOT LIKE '@%%'
                  )
                )
            ),
            (SELECT hostname FROM relayhosts
            LEFT OUTER JOIN domain ON domain.relayhost = relayhosts.id
              WHERE relayhosts.active = '1'
                AND (domain.domain = '%d'
                  OR domain.domain IN (
                    SELECT target_domain FROM alias_domain
                      WHERE alias_domain = '%d'
                  )
                )
            )
          )
        ) AS transport_view;

    - name: tls_enforce_in_policy.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT IF(EXISTS(
          SELECT 'TLS_ACTIVE' FROM alias
            LEFT OUTER JOIN mailbox ON mailbox.username = alias.goto
              WHERE (address='%s'
                OR address IN (
                  SELECT CONCAT('%u', '@', target_domain) FROM alias_domain
                    WHERE alias_domain='%d'
                )
              ) AND JSON_UNQUOTE(JSON_VALUE(attributes, '$.tls_enforce_in')) = '1' AND mailbox.active = '1'
          ), 'reject_plaintext_session', NULL) AS 'tls_enforce_in';

    - name: tls_policy_override_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT(policy, ' ', parameters) AS tls_policy FROM tls_policy_override WHERE active = '1' AND dest = '%s'

    - name: transport_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT('smtp_via_transport_maps:', nexthop) AS transport FROM transports
          WHERE active = '1'
          AND destination = '%s';

    - name: virtual_alias_domain_catchall_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT goto FROM alias, alias_domain
        WHERE alias_domain.alias_domain = '%d'
          AND alias.address = CONCAT('@', alias_domain.target_domain)
          AND alias.active = 1 AND alias_domain.active='1'

    - name: virtual_alias_domain_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT username FROM mailbox, alias_domain
        WHERE alias_domain.alias_domain = '%d'
          AND mailbox.username = CONCAT('%u', '@', alias_domain.target_domain)
          AND (mailbox.active = '1' OR mailbox.active = '2')
          AND alias_domain.active='1'

    - name: virtual_alias_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT goto FROM alias
        WHERE address='%s'
          AND (active='1' OR active='2');

    - name: virtual_domains_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT alias_domain from alias_domain WHERE alias_domain='%s' AND active='1'
        UNION
        SELECT domain FROM domain
          WHERE domain='%s'
            AND active = '1'
            AND backupmx = '0'

    - name: virtual_mailbox_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT CONCAT(JSON_UNQUOTE(JSON_VALUE(attributes, '$.mailbox_format')), mailbox_path_prefix, '%d/%u/') 
          FROM mailbox 
          WHERE username='%s' AND (active = '1' OR active = '2')

    - name: virtual_relay_domain_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT domain FROM domain WHERE domain='%s' AND backupmx = '1' AND active = '1'

    - name: virtual_resource_maps.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT 'null@localhost' FROM mailbox
          WHERE kind REGEXP 'location|thing|group' AND username = '%s';

    - name: virtual_sender_acl.cf
      <<: *DATABASE_DEFAULTS
      query: |
        SELECT goto FROM alias
          WHERE id IN (
              SELECT COALESCE (
                (
                  SELECT id FROM alias
                    WHERE address='%s'
                    AND (active='1' OR active='2')
                ), (
                  SELECT id FROM alias
                    WHERE address='@%d'
                    AND (active='1' OR active='2')
                )
              )
            )
            AND active='1'
            AND (domain IN
              (SELECT domain FROM domain
                WHERE domain='%d'
                  AND active='1')
              OR domain in (
                SELECT alias_domain FROM alias_domain
                  WHERE alias_domain='%d'
                    AND active='1'
              )
            )
          UNION
          SELECT logged_in_as FROM sender_acl
            WHERE send_as='@%d'
              OR send_as='%s'
              OR send_as='*'
              OR send_as IN (
                SELECT CONCAT('@',target_domain) FROM alias_domain
                  WHERE alias_domain = '%d')
              OR send_as IN (
                SELECT CONCAT('%u','@',target_domain) FROM alias_domain
                  WHERE alias_domain = '%d')
              AND logged_in_as NOT IN (
                SELECT goto FROM alias
                  WHERE address='%s')
          UNION
          SELECT username FROM mailbox, alias_domain
            WHERE alias_domain.alias_domain = '%d'
              AND mailbox.username = CONCAT('%u','@',alias_domain.target_domain)
              AND (mailbox.active = '1' OR mailbox.active ='2')
              AND alias_domain.active='1';

      - name: virtual_spamalias_maps.cf
        <<: *DATABASE_DEFAULTS
        query: |
          SELECT goto FROM spamalias
          WHERE address='%s'
            AND validity >= UNIX_TIMESTAMP()

postfix_proxy:
  read_maps:
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/sasl_passwd_maps_transport_maps.cf
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/mbr_access_maps.cf
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/tls_enforce_in_policy.cf
    - $sender_dependent_default_transport_maps
    - ...
    - $smtp_sasl_password_maps

postfix_relay:  
  domains: proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_relay_domain_maps.cf
  recipient_maps: proxy:mysql:{{ postfix_virtual_directory }}/mysql/relay_recipient_maps.cf

postfix_sender:
  dependent_default_transport_maps:
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/sender_dependent_default_transport_maps.cf

postfix_smtp:
  sasl:
    password_maps_file: proxy:mysql:{{ postfix_virtual_directory }}/mysql/sasl_passwd_maps_sender_dependent.cf
  tls:
    policy_maps_file: proxy:mysql:{{ postfix_virtual_directory }}/mysql/tls_policy_override_maps.cf

postfix_smtpd:
  recipient_restrictions:
    - check_recipient_mx_access proxy:mysql:{{ postfix_virtual_directory }}/mysql/mbr_access_maps.cf
    - permit_sasl_authenticated
    - permit_mynetworks
    - check_recipient_access proxy:mysql:{{ postfix_virtual_directory }}/mysql/tls_enforce_in_policy.cf
    - reject_invalid_helo_hostname
    - reject_unauth_destination
  sender_login_maps:
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_sender_acl.cf

postfix_virtual:
  alias_maps_files:
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_alias_maps.cf
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_resource_maps.cf
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_spamalias_maps.cf
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_alias_domain_maps.cf
  mailbox_domains: proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_domains_maps.cf
  mailbox_maps: proxy:mysql:{{ postfix_virtual_directory }}/mysql/virtual_mailbox_maps.cf

postfix_recipient:
  canonical_maps:
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/recipient_canonical_maps.cf

postfix_transport:
  maps_files:
    - pcre:/opt/postfix/conf/custom_transport.pcre
    - pcre:/opt/postfix/conf/local_transport
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/relay_ne.cf
    - proxy:mysql:{{ postfix_virtual_directory }}/mysql/transport_maps.cf
```
