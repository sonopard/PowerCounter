#!/bin/bash
curl \
    -H "ContentType: application/json" \
    -X POST \ 
    -d '{"address": 0x23, "bank":0}' \ 
    http://localhost:8080/powercounter/tick
