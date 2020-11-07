#!/bin/bash
KEY="ddns.key"
NS="m17ns.tarxvf.tech"
ZONE="m17ref.tarxvf.tech"
REFNAME="$1"
REFHOST="$2"
HOSTENTRY=$REFNAME.$ZONE
PORT=17000

nsupdate -k $KEY <<EOF
server $NS.
zone $ZONE.
update add _m17ref._udp.$HOSTENTRY 10 IN SRV 20 20 $PORT $REFHOST
send
EOF
#update delete $HOST.$ZONE A
#update add $HOST.$ZONE 10 A $IP

