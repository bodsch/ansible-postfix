
# `main.cf` 

## relay

```yaml
postfix_relay:
  clientcerts: ""
  delivery_slot_cost: ""                            # $default_delivery_slot_cost
  delivery_slot_discount: ""                        # $default_delivery_slot_discount
  delivery_slot_loan: ""                            # $default_delivery_slot_loan
  destination_concurrency_failed_cohort_limit: ""   # $default_destination_concurrency_failed_cohort_limit
  destination_concurrency_limit: ""                 # $default_destination_concurrency_limit
  destination_concurrency_negative_feedback: ""     # $default_destination_concurrency_negative_feedback
  destination_concurrency_positive_feedback: ""     # $default_destination_concurrency_positive_feedback
  destination_rate_delay: ""                        # $default_destination_rate_delay
  destination_recipient_limit: ""                   # $default_destination_recipient_limit
  domains: ""                                       # ${{$compatibility_level} < {2} ? {$mydestination} : {}}
  domains_reject_code: ""                           # 554
  extra_recipient_limit: ""                         # $default_extra_recipient_limit
  initial_destination_concurrency: ""               # $initial_destination_concurrency
  minimum_delivery_slots: ""                        # $default_minimum_delivery_slots
  recipient_limit: ""                               # $default_recipient_limit
  recipient_maps: ""                                #
  recipient_refill_delay: ""                        # $default_recipient_refill_delay
  recipient_refill_limit: ""                        # $default_recipient_refill_limit
  transport: ""                                     # relay
  transport_rate_delay: ""                          # $default_transport_rate_delay
  #
  use_tls: false
  mxlookup: false
  host: ''                                          # mail.test.com
  port: 587                                         # 587
  domains_file: ''
  recipient_maps_file: ''
```

