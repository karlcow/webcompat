#!/bin/sh
# Script to add a UA override to B2G
# Based on Dave Hyland's script https://gist.github.com/2656232
# Based on Lawrence Mandel's script https://gist.github.com/lmandel/4291503
# Put at https://github.com/karlcow/webcompat/blob/master/moz/mozua.sh
# Options:
#   remove - removes the override
# Usage:
#   ./mozua.sh add example.com
#   ./mozua.sh remove example.com
#   ./mozua.sh list example

LOCAL_USER_JS=/tmp/user.js
LOCAL_ORIG_USER_JS=/tmp/orig-user.js
PROFILE_DIR=/system/b2g/defaults/pref
REMOTE_USER_JS=${PROFILE_DIR}/user.js
ORIGINAL_PREF_URL='https://raw.github.com/mozilla-b2g/gaia/master/build/ua-override-prefs.js'

echo "FOR UA override on Firefox OS 1.0, 1.1"
echo "UA override on Firefox OS 1.2+ has a different mechanism"
# explaining the command
if [ $# != 2 ]; then
    echo ""
    echo "Usage: mozua.sh"
    echo ""
    echo "This program:-"
    echo "    mozua.sh add    example.com"
    echo "    mozua.sh remove example.com"
    echo "    mozua.sh remove all         # It removes everything"
    echo "    mozua.sh list   example"
    echo "    mozua.sh list   all"
    echo "    mozua.sh reset  all         # It restarts from scratch"
    echo "==============================="
    echo "Improve it!"
    echo "https://github.com/karlcow/webcompat/blob/master/moz/mozua.sh"
    exit 1
fi

# remove any previous files
rm -f ${LOCAL_USER_JS} ${LOCAL_USER_JS}.tmp ${LOCAL_ORIG_USER_JS}
# pull from the device to a local tmp directory
adb pull ${REMOTE_USER_JS} ${LOCAL_USER_JS}

# remove a ua from the list
if [ ${1} = "remove" ]
then
    # if all remove everything
    if [ ${2} = "all" ]
    then
        echo "Removing every UA domains override."
        grep -v 'pref("general.useragent.override.' ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    # if pattern foo list everything matching foo and quit.
    else
        # removing a specific domain
        echo "Removing UA override for ${2}"
        # Removing the matching UA
        grep -v ${2} ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    fi
# add a ua to the list
elif [ ${1} = "add" ]
then
    # adding fennec. Probably would be to have more options.
    echo "Adding fennec UA override for ${2}"
    # we should probably instead trying to test and then add.
    grep -v ${2} ${LOCAL_USER_JS} > ${LOCAL_USER_JS}.tmp
    ua=fennec
    echo 'pref("general.useragent.override.'${2}'", "\Mobile#(Android; Mobile");' >> ${LOCAL_USER_JS}.tmp
# list domains in the list
elif [ ${1} = "list" ]
then
    # if all list everything and quit. no need to reboot
    if [ ${2} = "all" ]
    then
        echo "Listing every domains"
        grep general.useragent.override ${LOCAL_USER_JS} | sed -e 's/^pref.*override\.\(.*\)", .* bug \(.*\)/\2 \1/'
    # if pattern foo list everything matching foo
    else
        echo "Listing domain matching ${2}"
        grep general.useragent.override ${LOCAL_USER_JS} | grep -i ${2} | sed -e 's/^pref.*override\.\(.*\)", .* bug \(.*\)/\2 \1/'
    fi
    # no need to reboot, we just quit
    exit 1
# reset to the original list
elif [ ${1} = "reset" ]
then
    # Fetching the current original list
    # !!!! this will brick more or less the device !!!!
    echo "NOT WORKING YET - Reset to the current production UA override list"
    exit 1
    #curl -o ${LOCAL_ORIG_USER_JS} ${ORIGINAL_PREF_URL}
    # We should test first if the file has been created
    #cp ${LOCAL_ORIG_USER_JS} ${LOCAL_USER_JS}.tmp
# avoiding surprises
else
    echo "Unknown command: ${1}"
    exit 1
fi

set -x
adb shell mount -o rw,remount /system
adb push ${LOCAL_USER_JS}.tmp ${REMOTE_USER_JS}
adb shell mount -o ro,remount /system
adb shell stop b2g && adb shell start b2g
#adb reboot
