#!/bin/sh
curl -s -c cookies.txt -F username=$1 -F password=$2 --insecure https://localhost:8080/login
