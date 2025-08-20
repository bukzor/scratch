#!/usr/bin/env bigquery
#standardSQL

WITH tmp AS (
  SELECT *
  from UNNEST(
    ARRAY<
      STRUCT<name STRING, count array<int64>>
    >
    [ ("one", [1, 2])
    , ("two", [2])
    ]
  )
)


SELECT tmp.* REPLACE (
  count as count
)
FROM
  tmp
, unnest(tmp.count) as count
