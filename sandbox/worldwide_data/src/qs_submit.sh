#!/bin/bash

: '
While the python script worked flawlessly, I still cant get 
the QS API to work, but keep this as a placeholder if Its 
able to work in the future.
'
date=$(printf '%(%Y-%m-%d)T\n' -1)

curl https://tools.wmflabs.org/quickstatements/api.php \
	-d action=import \
	-d submit=1 \
	-d username=${WIKIDATA_USER} \
	--data-raw "token=${WIKIDATA_TOKEN}" \
	--data-urlencode data@${date}.qs
