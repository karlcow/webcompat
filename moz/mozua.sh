#!/bin/sh
# Script to add a UA override to B2G
# Based on Dave Hyland's script https://gist.github.com/2656232
# Based on Lawrence Mandel's script https://gist.github.com/lmandel/4291503
# Put at https://github.com/karlcow/webcompat/moz/mozua.sh
# Options:
#   remove - removes the override
# Usage:
#   ./mozua.sh add example.com
#   ./mozua.sh remove example.com
#   ./mozua.sh list example

LOCAL_USER_JS=/tmp/user.js
PROFILE_DIR=/system/b2g/defaults/pref
REMOTE_USER_JS=${PROFILE_DIR}/user.js

# explaining the command
if [ $# != 2 ]; then
    echo ""
    echo "Usage: mozua.sh"
    echo ""
    echo "This program:-"
    echo "    mozua.sh add    example.com"
    echo "    mozua.sh remove example.com"
    echo "    mozua.sh list   example"
    echo "    mozua.sh list   all"
    echo "==============================="
    echo "Improve it!"
    echo "https://github.com/karlcow/webcompat/moz/mozua.sh"
    exit 1
fi

# remove any previous files
rm -f ${LOCAL_USER_JS}
# pull from the device to a local tmp directory
adb pull ${REMOTE_USER_JS} ${LOCAL_USER_JS}


# remove a ua from the list
if [ ${1} == "remove" ]
then
    echo "Removing UA override for ${2}"
    ua=""
# add a ua to the list
elif [ ${1} == "add" ]
then
    echo "Adding fennec UA override for ${2}"
    ua=fennec
# list domains in the list
elif [ ${1} == "list" ]
then
    # if all list everything and quit. no need to reboot
    if [ ${2} == "all" ]
    then
        echo "Listing every domains"
        grep general.useragent.override ${LOCAL_USER_JS} | sed -e 's/^pref.*override\.\(.*\)", .* bug \(.*\)/\2 \1/'
        exit 1
    # if pattern foo list everything matching foo and quit.
    else
        echo "Listing domain matching ${2}"
        grep general.useragent.override ${LOCAL_USER_JS} | grep -i ${2} | sed -e 's/^pref.*override\.\(.*\)", .* bug \(.*\)/\2 \1/'
        exit 1
    fi
# avoiding surprises
else
    echo "Unknown command: ${1}"
    exit 1
fi
grep -v ${2} ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
if [ "${ua}" != "" ]
then
    echo 'pref("general.useragent.override.'${2}'", "\Mobile#(Android; Mobile");' >> ${LOCAL_USER_JS}.tmp
fi

set -x
adb shell mount -o rw,remount /system
adb push ${LOCAL_USER_JS}.tmp ${REMOTE_USER_JS}
adb shell mount -o ro,remount /system
adb shell stop b2g && adb shell start b2g
#adb reboot
