#!/bin/bash

Run() {
    ( ../scrcpy-win64-v2.0/scrcpy.exe \
        --stay-awake \
        --turn-screen-off \
        --show-touches \
        --power-off-on-close \
        --window-x=960 --window-y=50 \
        --window-width=461 --window-height=976 ) & pid=$!

    sleep 15

    echo "Execute ProjectSekaiDaily"
    python main.py --debug true --routine "ProjectSekaiDaily"
    
    echo "Execute HeavenBurnsRedDaily"
    python main.py --debug true --routine "HeavenBurnsRedDaily"
    
    echo "Execute Deemo2Daily"
    python main.py --debug true --routine "Deemo2Daily"
    
    echo "Execute SinoaliceDaily"
    python main.py --debug true --routine "SinoaliceDaily"

    kill "${pid}"
}

(
    SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

    cd "${SCRIPTPATH}/../"
    echo "pwd = $(pwd)"

    SLEEP_SECONDS="21600"
    while true
    do
        echo "Current Time = $(date '+%Y-%m-%d %T'), "
        Run || echo "Failed to Run" # TODO: Send mail when failed
        echo "Done. Next Run = $(date --date="+${SLEEP_SECONDS} seconds" '+%Y-%m-%d %T')"
        sleep "${SLEEP_SECONDS}"
    done
)