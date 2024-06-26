#!/bin/bash

Run() {
    local has_failure=""
    local return_code=""
    local failed_routines=""

    ( "${SCRCPY}" \
        --stay-awake \
        --turn-screen-off \
        --show-touches \
        --power-off-on-close \
        --window-x=960 --window-y=50 \
        --window-width=461 --window-height=976 ) & pid=$!

    sleep 15
    
    echo "Execute HeavenBurnsRedDaily"
    python main.py --debug true --routine "HeavenBurnsRedDaily"
    return_code=$?
    if [[ "${return_code}" != "0" ]]; then
        echo "has_failure!"
        has_failure="true"
        failed_routines="${failed_routines}, HeavenBurnsRedDaily"
    fi
    
    echo "Execute ProjectSekaiDaily"
    python main.py --debug true --routine "ProjectSekaiDaily"
    return_code=$?
    if [[ "${return_code}" != "0" ]]; then
        echo "has_failure!"
        has_failure="true"
        failed_routines="${failed_routines}, ProjectSekaiDaily"
    fi 

    echo "Execute Deemo2Daily"
    python main.py --debug true --routine "Deemo2Daily"
    return_code=$?
    if [[ "${return_code}" != "0" ]]; then
        echo "has_failure!"
        has_failure="true"
        failed_routines="${failed_routines}, Deemo2Daily"
    fi
    
    echo "Execute SinoaliceDaily"
    python main.py --debug true --routine "SinoaliceDaily"
    return_code=$?
    if [[ "${return_code}" != "0" ]]; then
        echo "has_failure!"
        has_failure="true"
        failed_routines="${failed_routines}, SinoaliceDaily"
    fi

    echo "Execute BlueArchive"
    python main.py --debug true --routine "BlueArchiveDaily"
    return_code=$?
    if [[ "${return_code}" != "0" ]]; then
        echo "has_failure!"
        has_failure="true"
        failed_routines="${failed_routines}, BlueArchiveDaily"
    fi

    kill "${pid}"

    if [[ "${has_failure}" == "true" ]]; then
        echo "has_failure, failed = [${failed_routines}]"
        SendFailureReport
    fi
}

SendFailureReport() {
    echo "Detect Failure, Send Failure Report"
    local screenshot=$(UploadLatestScreenShot "$(pwd)/ScreenShots")
    echo "Screenshot = ${screenshot}"
    SendMail "${SENDGRID_TO_MAIL}" "${SENDGRID_FROM_MAIL}" "Failure Detected: $(date '+%Y-%m-%d %T')" "<p>Screenshot = ${screenshot}</p>" "${SENDGRID_API_KEY}"
    echo "Send Failure Report Done" 
}

EchoEnv() {
    echo "SENDGRID_API_KEY = ${SENDGRID_API_KEY}"
    echo "SENDGRID_TO_MAIL = ${SENDGRID_TO_MAIL}"
    echo "SENDGRID_FROM_MAIL = ${SENDGRID_FROM_MAIL}"
    echo "SCRCPY = ${SCRCPY}"
}

PrepareUpload() {
    local now=$1
    local SEVEN_ZIP="/c/Program Files/7-Zip/7z.exe"
    local backup_dir="backups/${now}"
    local backup_filename="../${now}.zip"
    
    mkdir -p "${backup_dir}"
    cp "log/"* "${backup_dir}"
    cp "ScreenShots/"* "${backup_dir}"

    (
        cd "${backup_dir}"
        "${SEVEN_ZIP}" a -tzip "${backup_filename}" "*"
    )

    rm -f "log/"*
    rm -f "ScreenShots/"*  
}

Backup() {
    local NOW=$(date +"%y-%m-%d-%H-%M-%S")
    local BACKUP_FILE="backups/${NOW}.zip"
    local RCLONE="./rclone.exe"

    PrepareUpload "${NOW}"
    "${RCLONE}" copy -v "${BACKUP_FILE}" "${RCLONE_REPO}"
}

(
    EchoEnv

    if [[ "${SENDGRID_API_KEY}" == "SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" || "${SENDGRID_API_KEY}" == "" ]]; then
        echo "you should call \`source scripts/.env.sh\` before start."
        exit -1
    fi

    SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

    cd "${SCRIPTPATH}/../"
    echo "pwd = $(pwd)"

    source "scripts/imgur.sh"
    source "scripts/utils.sh"

    SLEEP_SECONDS="21600"
    RUN_AT_START="${RUN_AT_START:-true}"
    while true
    do
        echo "Current Time = $(date '+%Y-%m-%d %T')"
        if [[ "${RUN_AT_START}" == "true" ]]; then
            Run
            Backup
            echo "Done. Next Run = $(date --date="+${SLEEP_SECONDS} seconds" '+%Y-%m-%d %T')"
        else
            echo "Disable run at start. Next Run = $(date --date="+${SLEEP_SECONDS} seconds" '+%Y-%m-%d %T')"
        fi
        RUN_AT_START="true"        
        sleep "${SLEEP_SECONDS}"
    done
)