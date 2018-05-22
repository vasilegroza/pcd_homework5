#!/bin/bash
export CONSUL_UI_BETA=true
consul agent -ui -server -bootstrap-expect=4 \
    -data-dir=./consul -node=watcher -bind=172.20.20.1 \
    -enable-script-checks=true -config-dir=./consul.d 

    
consul join 172.20.20.10
consul join 172.20.20.11
consul join 172.20.20.12
consul join 172.20.20.13