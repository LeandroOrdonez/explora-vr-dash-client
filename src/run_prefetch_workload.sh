#!/bin/bash

if [ "$ENABLE_TC" == "true" ]
then
    SIP=$(getent hosts ${CACHE_HOST} | cut -d' ' -f1)
    echo "src/traffic-control.sh -o --delay=${LATENCY} --jitter=${JITTER} --uspeed=${BANDWIDTH} --dspeed=${BANDWIDTH} ${SIP}"
    sudo src/traffic-control.sh -o --delay=${LATENCY} --jitter=${JITTER} --uspeed=${BANDWIDTH} ${SIP}
fi

for u in 25 27 28 38 41 44
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 1";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 1;
        done
    done
done

for u in 4 5 9 13 20 26
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 2";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 2;
        done
    done
done

for u in 7 14 18 34 40 46
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 3";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 3;
        done
    done
done

for u in 10 16 17 30 33 47
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 4";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 4;
        done
    done
done

for u in 1 6 12 31 32 35
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 5";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 5;
        done
    done
done

for u in 2 3 22 36 37 45
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 6";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 6;
        done
    done
done

for u in 11 19 23 24 42 48
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 7";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 7;
        done
    done
done

for u in 8 15 21 29 39 43
do
    for v in 0 2 4
    do
        for k in -1
        do
            echo "python src/vr_client.py --user ${u} --video ${v} --k ${k} --prefetch --fold 8";
            python src/vr_client.py --user $u --video $v --k $k --prefetch --fold 8;
        done
    done
done

