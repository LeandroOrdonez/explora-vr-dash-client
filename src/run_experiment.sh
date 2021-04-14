#!/bin/bash

./run_prefetch_workload.sh
sleep 30
LATENCY=15
./run_no_prefetch_workload.sh
