#!/bin/sh

set -eux

curl -sSL --cookie ./getsentry.net_cookies.txt https://freight.getsentry.net/api/0/deploys/ |
  jq '
    .[]
    | select(.app.name | startswith("getsentry-"))
    | .user.name
  ' |
  sort |
  uniq -c |
  sort -n \
;
