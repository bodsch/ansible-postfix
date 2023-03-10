
# `main.cf` 

## virtual

```yaml
postfix_virtual:
  aliases: []
  #   - virtual: webmaster@yourdomain.com
  #     alias: personal_email@gmail.com
  #   - virtual: billandbob@yourdomain.com
  #     alias: bill@gmail.com, bob@gmail.com
  #   - virtual: ann-katrin@yourdomain.com
  #     aliases:
  #       - ann@gmail.com
  #       - bob@gmail.com
  #       - katrin@gmail.com
  alias_address_length_limit: ""                    # 1000
  alias_domains: []                                 # $virtual_alias_maps
  alias_expansion_limit: ""                         # 1000
  alias_maps: []
  alias_recursion_limit: ""                         # 1000
  delivery_slot_cost: ""                            # $default_delivery_slot_cost
  delivery_slot_discount: ""                        # $default_delivery_slot_discount
  delivery_slot_loan: ""                            # $default_delivery_slot_loan
  delivery_status_filter: ""                        # $default_delivery_status_filter
  destination_concurrency_failed_cohort_limit: ""   # $default_destination_concurrency_failed_cohort_limit
  destination_concurrency_limit: ""                 # $default_destination_concurrency_limit
  destination_concurrency_negative_feedback: ""     # $default_destination_concurrency_negative_feedback
  destination_concurrency_positive_feedback: ""     # $default_destination_concurrency_positive_feedback
  destination_rate_delay: ""                        # $default_destination_rate_delay
  destination_recipient_limit: ""                   # $default_destination_recipient_limit
  extra_recipient_limit: ""                         # $default_extra_recipient_limit
  gid_maps: []
  initial_destination_concurrency: ""               # $initial_destination_concurrency
  mailbox_base: ""                                  # (default: empty)
  mailbox_domains: ""                               # $virtual_mailbox_maps
  mailbox_limit: ""                                 # 51200000
  mailbox_lock: []                                  # [fcntl, dotlock]
  mailbox_maps: []
  minimum_delivery_slots: ""                        # $default_minimum_delivery_slots
  minimum_uid: ""                                   # 100
  recipient_limit: ""                               # $default_recipient_limit
  recipient_refill_delay: ""                        # $default_recipient_refill_delay
  recipient_refill_limit: ""                        # $default_recipient_refill_limit
  transport: ""                                     # virtual
  transport_rate_delay: ""                          # $default_transport_rate_delay
  uid_maps: []
```
