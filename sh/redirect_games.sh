#!/bin/bash
exec 10<> <(:)
exec 11<> <(:)
exec 12<> <(:)

grep --color 12 <&12 &
grep --color 11 <&11 &

tee /proc/self/fd/11 /proc/self/fd/12 <&10 &

echo 11 12 >&10
