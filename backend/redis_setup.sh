#!/bin/bash
echo "redis for chaching port 6379" &
redis-server --port 6379 &
echo "redis for celery port 6380" &
redis-server --port 6380 &





