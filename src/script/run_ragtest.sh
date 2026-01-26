#!/bin/sh
set -e

cd /home/ec2-user/repo/repo01/product

/usr/bin/docker compose exec aidemo01-api \
  python src/script/ragtest.py
