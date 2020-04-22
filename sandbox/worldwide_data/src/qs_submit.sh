#!/bin/bash

date=$(printf '%(%Y-%m-%d)T\n' -1)

curl https://tools.wmflabs.org/quickstatements/api.php \
	-d action=import \
	-d submit=1 \
	-d username=${WIKIDATA_USER} \
	--data-raw "token=${WIKIDATA_TOKEN}" \
	--data-urlencode data@${date}.qs
