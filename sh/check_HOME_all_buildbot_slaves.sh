#!/bin/bash

echo /etc/systems.d/nodes/bb* | 
	xargs -n1 basename |
	egrep 'bb(28|29|31)sv' |
	xargs --replace sh -c '
		ssh -A {} '"'"'
			echo {}:
			pgrep -f buildslave |
				sudo xargs --replace={2} sh -c '"'"'"'"'"'"'"'"'
					echo $(
						cat /proc/{2}/environ |
						xargs -0 -n1 |
						grep ^HOME=
						cat /proc/{2}/cmdline
					)
			'"'"'"'"'"'"'"'"'
		'"'"' || true
	'
