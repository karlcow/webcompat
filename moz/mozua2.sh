#!/bin/sh
# Script to add manage UA override to B2G 1.2+
# Karl Dubost - 2013 © - MIT Licence

LOCAL_USER_JS=/tmp/user.js
LOCAL_ORIG_USER_JS=/tmp/orig-user.js
PROFILE_DIR=/system/b2g/defaults/pref
REMOTE_USER_JS=${PROFILE_DIR}/user.js

function preparing {
    # remove any previous files
    rm -f ${LOCAL_USER_JS} ${LOCAL_USER_JS}.tmp ${LOCAL_ORIG_USER_JS}    
    # pull from the device to a local tmp directory
    adb pull ${REMOTE_USER_JS} ${LOCAL_USER_JS}
}

function helpmsg {
    # Print the list of arguments
    echo "TODO Manual to create"
}

function overridestatus {
    # Check the status of override
    PREFOVERRIDE=`grep useragent.updates.enabled ${LOCAL_USER_JS}`
    if [[ "$PREFOVERRIDE" =~ "false" ]]; then
        echo False
    else
        echo True
    fi
}

function override {
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

function error {
    # error message
    echo "This is not a valid feature"
}

function activate {
    # Activate UA override
    echo "Activate UA override"
    grep -v "useragent.updates.enabled" ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    echo 'pref("general.useragent.updates.enabled", true);' >> ${LOCAL_USER_JS}.tmp
    pushtodevice
}

function stop {
    # Stop UA Override
    echo "Stop UA override"
    grep -v "useragent.updates.enabled" ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    echo 'pref("general.useragent.updates.enabled", false);' >> ${LOCAL_USER_JS}.tmp
    pushtodevice
}

function pushtodevice {
    # Upload the new prefs
    echo "Pushing to device"
    set -x
    adb shell mount -o rw,remount /system
    adb push ${LOCAL_USER_JS}.tmp ${REMOTE_USER_JS}
    adb shell mount -o ro,remount /system
    restart
}

function restart {
    # Create a soft reboot
    echo "Restart the device (software)"
    adb shell stop b2g && adb shell start b2g
}

function reboot {
    # Create a hard reboot
    echo "Restart the device (hardware)"
    adb reboot
}

echo "========================================="
echo "UA override management on Firefox OS 1.2+"
echo "========================================="

# Main 
if [[ $# != 2 ]]; then
    helpmsg
    exit 1
fi

# Saving locally the files from the device
preparing
# Going through the options
if   [[ ${1} == "override" ]]; then
    override ${2}
elif [[ ${1} == "list" ]]; then
    echo "TODO list UA override for " ${2}
elif [[ ${1} == "add" ]]; then
    echo "TODO add UA override for " ${2}
elif [[ ${1} == "remove" ]]; then
    echo "TODO remove UA override for " ${2}
else
    error
    helpmsg
fi
# End
echo "Bye!"
