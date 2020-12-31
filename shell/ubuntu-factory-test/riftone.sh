#!/bin/bash

##################################################################################################################################
#                                                       测试流程
# 测试准备
#       1. 插上HDMI
#       2. 插上U盘
#       3. 插上网线
#       4. 插上SD卡
#       5. 烧录好测试程序
# 测试准备完成以后再上电
#
# 测试流程
#       1. 测试USB(自动测试)
#       2. 测试TF卡(自动测试)
#       3. 测试网口(自动测试)
#       3. 测试LTE模块(自动测试)
#
# 测试结果
#       显示PASS则为测试通过,显示FAIL则为测试失败
##################################################################################################################################


BLACK="\e[0;30m"
BOLDBLACK="\e[1;30m"
RED="\e[0;31m"
BOLDRED="\e[1;31m"
GREEN="\e[0;32m"
BOLDGREEN="\e[1;32m"
YELLOW="\e[0;33m"
BOLDYELLOW="\e[1;33m"
BLUE="\e[0;34m"
BOLDBLUE="\e[1;34m"
MAGENTA="\e[0;35m"
BOLDMAGENTA="\e[1;35m"
CYAN="\e[0;36m"
BOLDCYAN="\e[1;36m"
WHITE="\e[0;37m"
BOLDWHITE="\e[1;37m"
ENDCOLOR="\e[0m"

TEST_PROGRESS=None
USB_TEST_RESULT=None
SD_TEST_RESULT=None
ETH_TEST_RESULT=None
WIFI_TEST_RESULT=None
LTE_TEST_RESULT=None

NETWORK_IFACE="wlan0"
WIFI_TEST_SSID="Namtso_5G"
WIFI_TEST_PIPE="/tmp/wifi_test_pipe"
WIFI_SIGNAL_THRESHOLD=80
WIFI_SIGNAL=
WIFI_TEST_COUNT=10
WIFI_TEST_FAIL_COUNT_MAX=2
WIFI_TEST_RESULT= # BROKEN/WEAK_SIGNAL/OK


DISPLAY_TTY_NUM=7
DISPLAY_TTY=/dev/tty$DISPLAY_TTY_NUM

export TERM=linux
chvt $DISPLAY_TTY_NUM


clear > $DISPLAY_TTY

show_menu_header() {
#   printf "\n\n" > $DISPLAY_TTY
    printf "\t\t\t\t${BOLDWHITE}Test Results${ENDCOLOR}\n" > $DISPLAY_TTY
}

# $1 message
# $2 color
show_msg() {
    printf "${2}${1}${ENDCOLOR}" > $DISPLAY_TTY
}

show_key_value() {
    KEY_COLOR=$BOLDWHITE
    VALUE_COLOR=$GREEN
    printf "\t\t\t${KEY_COLOR}%-25s:${ENDCOLOR}${VALUE_COLOR}\t%-20s${ENDCOLOR}\n" "$1" "$2" > $DISPLAY_TTY
}


show_menu_item() {
    if [ "$2" == "PASS" ]; then
        COLOR="$BOLDGREEN"
    else
        COLOR="$BOLDRED"
    fi

    printf "\t\t\t${BOLDYELLOW}%-25s:${ENDCOLOR}\t${COLOR}%-10s${ENDCOLOR}\n" "$1" "$2" > $DISPLAY_TTY
}

show_progress() {
    printf "\t\t\t${BOLDYELLOW}TESTING${ENDCOLOR}:${BOLDGREEN}%-25s${ENDCOLOR}\n" "$1" > $DISPLAY_TTY
}

show_result_menu() {
    clear > $DISPLAY_TTY
    show_progress "$TEST_PROGRESS"
    show_menu_header
    show_menu_item "USB"            "$USB_TEST_RESULT"
    show_menu_item "SD Card"        "$SD_TEST_RESULT"
    show_menu_item "Ethernet"       "$ETH_TEST_RESULT"
    show_menu_item "Wi-Fi"          "$WIFI_TEST_RESULT"
    show_menu_item "LTE"            "$LTE_TEST_RESULT"
    show_msg "\t\t\t=================================================\n" "$BLUE"
    source /etc/fenix-release
    show_key_value "Board" "$BOARD"
    show_key_value "Firmware Version" "$IMAGE_RELEASE_VERSION"
    show_key_value "Ethernet IP Address" "$ETH_IP_ADDRESS"
    show_key_value "Ethernet MAC Address" "$ETH_MAC_ADDRESS"
}

test_sd_card() {
    if [ -b /dev/mmcblk1 ] && [ -b /dev/mmcblk1p1 ]; then
        SD_TEST_RESULT="PASS"
    else
        SD_TEST_RESULT="FAIL"
    fi
}

test_ethernet() {
    ETH_IP_ADDRESS=`ifconfig eth0 | grep -w inet | awk  '{print $2}'`
    ETH_MAC_ADDRESS=`ifconfig eth0 | grep -w ether | awk  '{print $2}'`
    if dmesg | grep -q "1Gbps/Full"; then
        IS_ETH_GB=Yes
    else
        IS_ETH_GB=No
    fi
    if [ -n "$ETH_IP_ADDRESS" ] && [ "$IS_ETH_GB" == Yes ]; then
        ETH_TEST_RESULT="PASS"
    else
        ETH_TEST_RESULT="FAIL"
    fi
}


test_usb() {
    if [ -b /dev/sda ] && [ -b /dev/sda1 ]; then
        USB_TEST_RESULT="PASS"
    else
        USB_TEST_RESULT="FAIL"
    fi
}



is_wifi_firmware_load_ok() {
    WIFI_STATUS=$(cat /sys/class/net/${NETWORK_IFACE}/operstate)      
    if [[ "$WIFI_STATUS" = "up" || "$WIFI_STATUS" = "dormant" ]]; then
        return 0
    fi
    return -1
}

get_wifi_signal() {
    WIFI_SIGNAL=$(nmcli d wifi list | grep "$WIFI_TEST_SSID" | awk '{print $6}')
}

check_wifi_connection() {
    WIFI_STATUS=$(cat /sys/class/net/${NETWORK_IFACE}/operstate)
    if [[ "$WIFI_STATUS" = "up" || "$WIFI_STATUS" = "dormant" ]]; then
        if /sbin/ifconfig "$NETWORK_IFACE" | grep "inet addr" > /dev/null; then
            return 0
        fi
    fi    
    return 255
}

test_wifi() {
    FAIL_COUNT=0
    is_wifi_firmware_load_ok || {
    # wifi is broken
    WIFI_TEST_RESULT="BROKEN"
#    echo "$WIFI_TEST_RESULT"
    WIFI_TEST_RESULT="FAIL"
    }

    COUNT=$WIFI_TEST_COUNT
    while (( "$COUNT" > 0 ))
    do
        get_wifi_signal
#        echo "wifi signal: $WIFI_SIGNAL"

        if [ "$WIFI_SIGNAL" == "" ] || [ "$WIFI_SIGNAL" -lt "$WIFI_SIGNAL_THRESHOLD" ]; then
            FAIL_COUNT=$((FAIL_COUNT + 1))
#            echo "Wi-Fi test fail: $FAIL_COUNT times."
            if [ "$FAIL_COUNT" -ge "$WIFI_TEST_FAIL_COUNT_MAX" ]; then
#                echo "Wi-Fi test failed!"
                break;
            fi
        fi

        sleep 0.1

        COUNT=$((COUNT - 1))
    done
    if [ "$FAIL_COUNT" -lt $WIFI_TEST_FAIL_COUNT_MAX ]; then
        # Wifi signal test ok
        WIFI_TEST_RESULT="PASS"
#        echo "$WIFI_TEST_RESULT"
    else
        # Wifi signal test failed
        WIFI_TEST_RESULT="FAIL"
#        echo "$WIFI_TEST_RESULT"
    fi

}

test_lte() {
    if dmesg | grep -q "GobiNet"; then
        lte_driver=Yes
    else
        lte_driver=No
    fi
    if [ "$lte_driver" == "Yes" ] && [ -c /dev/ttyUSB0 ] && [ -c /dev/ttyUSB1 ] && [ -c /dev/ttyUSB2 ] && [ -c /dev/ttyUSB3 ]; then
        LTE_TEST_RESULT=PASS
    else
        LTE_TEST_RESULT=FAIL
    fi
}

#############################################################################################################################

check_wifi_connection && nmcli d disconnect $NETWORK_IFACE

TEST_PROGRESS="SD-CARD"
show_result_menu
test_sd_card


TEST_PROGRESS="ETHERNET"
show_result_menu
test_ethernet


TEST_PROGRESS="USB"
show_result_menu
test_usb


TEST_PROGRESS="WIFI"
show_result_menu
test_wifi


TEST_PROGRESS="LTE"
show_result_menu
test_lte

show_result_menu

sleep 2

TEST_PROGRESS="Done"
show_result_menu
