#!/bin/bash
set -euo pipefail

# По умолчанию чистим Wireguard1; другой интерфейс передаётся первым аргументом.
interface="${1:-Wireguard1}"
# Ошибка SSH останавливает скрипт до вывода команд удаления.
routes=$(ssh keenetic 'show ip route')

printf '%s\n' "$routes" | awk -v interface="$interface" '
    $1 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+$/ &&
    $2 == "0.0.0.0" && $3 == interface {
        if ($1 == "0.0.0.0/0" || $1 == "1.1.1.1/32" ||
            $1 == "8.8.8.8/32" || $1 == "10.40.0.0/24") next
        if (!seen[$1]++) print "no ip route " $1 " " interface
    }
'
