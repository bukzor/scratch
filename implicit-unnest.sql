#!/usr/bin/env bigquery
#standardSQL

WITH Coordinates AS (
  SELECT [1,2] AS position
)
SELECT results
FROM
  Coordinates
, Coordinates.position AS results
