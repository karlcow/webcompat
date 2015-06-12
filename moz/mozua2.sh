#!/bin/sh
# Script to add manage UA override to B2G 1.2+
# Karl Dubost - 2013 © - MIT Licence

LOCAL_USER_JS=/tmp/user.js
LOCAL_ORIG_USER_JS=/tmp/orig-user.js
# TODO: Change this for /data/b2g/mozilla/*.default/
# The user profile is
# /data/b2g/mozilla/something.default/prefs.js
PROFILE_DIR=/system/b2g/defaults/pref
REMOTE_USER_JS=${PROFILE_DIR}/user.js
SERVER_UA_LIST='https://hg.mozilla.org/mozilla-central/raw-file/tip/b2g/app/ua-update.json.in'
LOCAL_UA_LIST=/tmp/server_ua.txt

preparing() {
    # remove any previous files
    rm -f ${LOCAL_USER_JS} ${LOCAL_USER_JS}.tmp ${LOCAL_ORIG_USER_JS} ${LOCAL_UA_LIST}
    # pull from the device to a local tmp directory
    adb pull ${REMOTE_USER_JS} ${LOCAL_USER_JS}
    # downloading the remote list of UA override
    curl -s ${SERVER_UA_LIST} -o ${LOCAL_UA_LIST}
}

helpmsg() {
    # Print the list of arguments
    cat << EOF
The List of UA overrides is controlled by a remote file located at:
https://hg.mozilla.org/mozilla-central/raw-file/tip/b2g/app/ua-update.json.in

In addition you still have the ability to add UA override
locally for testing.

Usage: mozua2.sh <options>

List of options:

on/off:
    Enable or disable the remote UA override list.

list <string>:
    Give a list of all domain names matchin the string
    having a UA override.

add <domain_name> <ua_string>:
    Add the domain_name to the local list of UA overrides
    using a specific User Agent string.

remove <domain_name>:
    Remove the domain_name from the local list of UA overrides.

EOF
}

overridestatus() {
    # Check the status of override
    PREFOVERRIDE=$(grep useragent.updates.enabled ${LOCAL_USER_JS})
    if [[ "$PREFOVERRIDE" =~ "false" ]]; then
        echo False
    else
        echo True
    fi
}

override() {
    if   [[ $1 == "on" ]]; then
        if [[ overridestatus == True ]]; then
            echo "UA override is already on!"
            exit 1
        fi
        activate
    elif [[ $1 = "off" ]]; then
        if [[ overridestatus == False ]]; then
            echo "UA override is already off!"
            exit 1
        fi
        stop
    else
        error
    fi
}

list() {
    local DOMAIN=${1}
    echo "UA override for" ${DOMAIN}
    grep -i ${DOMAIN} ${LOCAL_UA_LIST} ${LOCAL_USER_JS}
    echo "TODO: better presentation and matching for search"
}

add() {
    local DOMAIN=${1}
    local UA=${2}
    remote_list=$(grep -i ${DOMAIN} ${LOCAL_UA_LIST} | sed -e 's/^ *//' -e 's/ *$//')
    user_list=$(grep -i general.useragent.override.${DOMAIN} ${LOCAL_USER_JS})
    if [[ -z "$remote_list" ]]; then
        if [[ -z "$user_list" ]]; then
            echo "@TODO: Adding UA override for" ${DOMAIN} "with User-Agent" ${UA}
        else
            echo "There is already a local UA override for this domain."
            echo "local:<$user_list>"
        fi
    else
        echo "There is already a remote UA override for this domain."
        echo "local:<$remote_list>"
    fi
    echo "@TODO: If yes display the current UA override"
    echo "@TODO: If no  add the UA override to the prefs file in /tmp"
    echo "@TODO: push to device"
    echo "@TODO: reboot the device"
    }


error() {
    # error message
    echo "This is not a valid feature"
}

activate() {
    # Activate UA override
    echo "Activate UA override"
    grep -v "useragent.updates.enabled" ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    echo 'pref("general.useragent.updates.enabled", true);' >> ${LOCAL_USER_JS}.tmp
    pushtodevice
}

stop() {
    # Stop UA Override
    echo "Stop UA override"
    grep -v "useragent.updates.enabled" ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    echo 'pref("general.useragent.updates.enabled", false);' >> ${LOCAL_USER_JS}.tmp
    pushtodevice
}

pushtodevice() {
    # Upload the new prefs
    echo "Pushing to device"
    set -x
    adb shell mount -o rw,remount /system
    adb push ${LOCAL_USER_JS}.tmp ${REMOTE_USER_JS}
    adb shell mount -o ro,remount /system
    restart
}

restart() {
    # Create a soft reboot
    echo "Restart the device (software)"
    adb shell stop b2g && adb shell start b2g
}

reboot() {
    # Create a hard reboot
    echo "Restart the device (hardware)"
    adb reboot
}

echo "========================================="
echo "UA override management on Firefox OS 1.2+"
echo "========================================="

# Main
if [[ $# < 2 || $# > 3 ]]; then
    helpmsg
    exit 1
fi

# Saving locally the files from the device
preparing
# Going through the options
if   [[ ${1} == "override" ]]; then
    override ${2}
elif [[ ${1} == "list" ]]; then
    list ${2}
elif [[ ${1} == "add" ]]; then
    add ${2} ${3}
elif [[ ${1} == "remove" ]]; then
    echo "TODO remove UA override for " ${2}
else
    error
    helpmsg
fi
# End
echo "Bye!"
