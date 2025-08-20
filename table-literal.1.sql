#!/usr/bin/env bigquery
#standardSQL

with example as (
  select *
  from UNNEST(
    ARRAY<
      STRUCT<user STRING, tests ARRAY<INT64>>
    >
    [ ("buck", [1,2,3])
    , ("max", [9,8])
    ]
  )
)

select example.*
from example


