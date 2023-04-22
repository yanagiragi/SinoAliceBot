#!/bin/bash

UploadLatestScreenShot() {
    local screenshot_dir_path=$1;
    local script_path;
    local screenshot_path;
    local uploaded_link;
    screenshot_path="$(find ${screenshot_dir_path} -maxdepth 1 -type f | head -n 1)"
    uploaded_link="$(UploadToImgur ${screenshot_path})"
    echo "${uploaded_link}"
}

SendMail () {
    local EMAIL_TO=$1
    local FROM_EMAIL=$2
    local SUBJECT=$3
    local CONTENT=$4
    local SENDGRID_API_KEY=$5

    local maildata="
    {
        \"personalizations\": [
            {
                \"to\": [
                    {
                        \"email\": \"${EMAIL_TO}\"
                    }
                ]
            }
        ],
        \"from\": {
            \"email\": \"${FROM_EMAIL}\"
        },
        \"subject\": \"${SUBJECT}\",
        \"content\": [
            {
                \"type\": \"text/html\",
                \"value\": \"${CONTENT}\"
            }
        ]
    }"
    
    curl --request POST \
        --url https://api.sendgrid.com/v3/mail/send \
        --header "authorization: Bearer ${SENDGRID_API_KEY}" \
        --header "Content-Type: application/json" \
        --data "${maildata}"
}