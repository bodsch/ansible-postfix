

```yaml
postfix_default:
  database_type: "hash"                             # hash
  delivery_slot_cost: ""                            # 5
  delivery_slot_discount: ""                        # 50
  delivery_slot_loan: ""                            # 3
  delivery_status_filter: ""
  destination_concurrency_failed_cohort_limit: ""   # 1
  destination_concurrency_limit: ""                 # 20
  destination_concurrency_negative_feedback: ""     # 1
  destination_concurrency_positive_feedback: ""     # 1
  destination_rate_delay: ""                        # 0s
  destination_recipient_limit: ""                   # 50
  extra_recipient_limit: ""                         # 1000
  filter_nexthop: ""
  minimum_delivery_slots: ""                        # 3
  privs: ""                                         # nobody
  process_limit: ""                                 # 100
  rbl_reply: ""                                     # $rbl_code Service unavailable; $rbl_class [$rbl_what] blocked using $rbl_domain${rbl_reason?; $rbl_reason}
  recipient_limit: ""                               # 20000
  recipient_refill_delay: ""                        # 5s
  recipient_refill_limit: ""                        # 100
  transport: ""                                     # smtp
  transport_rate_delay: ""                          # 0s
  verp_delimiters: ""                               # +=
``
