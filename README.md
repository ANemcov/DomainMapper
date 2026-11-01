## Domain Mapper

### Запуск всех профилей Keenetic

Из корня проекта, после установки зависимостей в `.venv`, с выключенным VPN ноутбука:

```bash
.venv/bin/python main.py -c keen-config.ini
```

Команда последовательно генерирует общий список, custom, YouTube и OpenAI,
затем объединяет их в `merged-routes.txt`. Итоговые команды применяются на роутере отдельно.
Подробности приведены в разделе «Генерация всех маршрутов Keenetic одной командой» ниже.

<details>
  <summary>Что нового (нажать, чтобы открыть)</summary>

- Реворк работы с DNS серверами. Прогрессбар. Разделение файла на части для некоторых форматов. Обновлена утилита Сonvert.
- Keenetic BAT формат сохранения. Небольшие изменения в интерфейсе. Некоторые доработки/улучшения.
- Доабвлены некоторые [оналйн кинотеатры](https://github.com/Ground-Zerro/DomainMapper/blob/main/platforms/dns-onlinetheater.txt). Запрос @Andrey_schumacher
- Добавлены списки от [ITDog](https://t.me/itdoginfo/36).
- Добавлен сервис xBox. Запрос @Deni5c
- Запуск в докере. Запрос [Запрос @andrejs82git](https://github.com/Ground-Zerro/DomainMapper/issues/21), [Реализация @MrEagle123](https://github.com/Ground-Zerro/DomainMapper/issues/21#issuecomment-2509565392)
- Опция в config.ini: не добавлять comment="%SERVICE_NAME%" при сохранении IP-адресов в mikrotik формате. [Запрос @ITNetSystem](https://github.com/Ground-Zerro/DomainMapper/issues/45) 
- Изменена кодиовка файла результатов на UTF-8 без BOM. [Запрос @Savanture](https://github.com/Ground-Zerro/DomainMapper/issues/54) 
- [Конвертер маршутов](https://github.com/Ground-Zerro/DomainMapper/tree/main/utilities) как отдельная утилита. [Запрос @Andrey999r](https://github.com/Ground-Zerro/DomainMapper/discussions/43) 
- Добавлен сервис Jetbrains. [Запрос @SocketSomeone](https://github.com/Ground-Zerro/DomainMapper/issues/40)
- Добавлен сервис Discord. [Запрос @AHuMex](https://github.com/Ground-Zerro/DomainMapper/issues/38)
- [Комбинированный режим объединения IP-адресов в подсеть.](https://github.com/Ground-Zerro/DomainMapper/issues/36)
- Возможность загрузки списков сервисов и DNS-серверов из локального файла. [Запрос @Noksa](https://github.com/Ground-Zerro/DomainMapper/issues/26) 
- Вспомагательные [утилиты](https://github.com/Ground-Zerro/DomainMapper/tree/main/utilities) для поиска субдоменов.
- Добавлен сервис Twitch. [Запрос @shevernitskiy](https://github.com/Ground-Zerro/DomainMapper/issues/31)
- Добавлен Yandex DNS сервер. [Запрос @Noksa](https://github.com/Ground-Zerro/DomainMapper/issues/26)
- Опция в config.ini: Отключить отображение сведений о загруженой конфигурации.
- Передача имени конфигурационного файла ключом в терминале/командной строке. [Запрос @Noksa](https://github.com/Ground-Zerro/DomainMapper/issues/25)
- Добавлен сервис Github Copilot. [Запрос @aspirisen](https://github.com/Ground-Zerro/DomainMapper/issues/23)
- Keenetic CLI формат сохранения. [Запрос @vchikalkin](https://github.com/Ground-Zerro/DomainMapper/pull/20)
- Wireguard формат сохранения. [Запрос @sanikroot](https://github.com/Ground-Zerro/DomainMapper/issues/18)
- Агрегация маршрутов до /24, /16. [Запрос @sergeeximius](https://github.com/Ground-Zerro/DomainMapper/issues/8)
- OVPN формат сохранения. [Запрос @SonyLo](https://github.com/Ground-Zerro/DomainMapper/pull/13)
- Mikrotik формат сохранения. [Запрос @Shaman2010](https://github.com/Ground-Zerro/DomainMapper/pull/9)

</details>

**Описание:** Инструмент на языке Python, предназначенный для разрешения DNS имен популярных веб-сервисов в IP-адреса.


<details>
  <summary>Поддерживаемые сервисы (нажать, чтобы открыть)</summary>

- [Antifilter - community edition](https://community.antifilter.download/)
- [ITDog Inside](https://github.com/itdoginfo/allow-domains)
- [ITDog Outside](https://github.com/itdoginfo/allow-domains)
- Youtube
- Facebook
- Openai
- Tik-Tok
- Instagram
- Twitter
- Netflix
- Bing
- Adobe
- Apple
- Google
- Torrent Trackers
- Search engines
- [Github сopilot](https://github.com/features/copilot)
- Twitch
- Discord
- Jetbrains
- Xbox
- Telegram
- Личный список

</details>


**Функции:**
- Преобразование доменных имен популярных сервисов в IP-адреса.
- Агрегация маршрутов в /16 (255.255.0.0) и /24 (255.255.255.0) подсети. Комбинированный режим /24 + /32.
- Фильтрация IP-адресов Cloudflare (опционально).
- Множество форматов сохранения результата.
- Разделение больших файлов на части для некоторых форматов.


**Ключевые особенности**
- Возможность выбора системного, публичного DNS-сервера или их комбинации.
- При разрешении доменного имени используется каждый из указанных DNS-серверов, при этом процесс продолжается до получения всех возможных IP-адресов, а не останавливается на первом успешном ответе.
- Автоматическое исключение дубликатов IP-адресов, а также "заглушек" (например, IP самих DNS-серверов, редиректов на `0.0.0.0` и `localhost`).
- Поддержка работы в "тихом" режиме без взаимодействия с пользователем - настройка через конфигурационный файл.
- В конфигурационном файле можно указать команду для автоматического запуска другого скрипта или программы по завершении работы.


###  Использование:

1. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```
2. Отредактируйте `config.ini` под свои задачи (опционально)

3. Запустите скрипт:

   ```bash
   python main.py
   ```


<details>
  <summary>Локальный режим работы (нажать, чтобы открыть)</summary>

В этом режиме списки DNS-серверов и сервисов загружаются из локальных файлов в папке со скриптом, а не из сети.

Для включения загрузки списка сервисов из локального файла `platformdb`, укажите `localplatform = yes` в config.ini.
- Формат файла `platformdb`: название сервиса и путь к локальному файлу через двоеточие.
Поддерживается работа как с файлами на локальной машине, так и их загрузка из сети по http(s).
Пример:
```
Torrent Truckers: platforms/dns-ttruckers.lst
Search engines: dns-search-engines.txt
Twitch: platforms/service/dns-twitch.txt
Adobe: https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/main/platforms/dns-adobe.txt
```

Для включения загрузки списка DNS-серверов из локального файла `dnsdb`, укажите `localdns = yes` в config.ini.
- Формат файла `dnsdb`: название DNS-сервера и его IP-адреса через двоеточие и пробел.
Важно - нужно обязательно указать два IP-адреса для каждого названия (можно один и тот же), это необходимо для правильной работы кода. 
Пример:
```
SkyDNS: 77.88.8.8 77.88.8.8
Alternate DNS: 76.76.19.19 76.223.122.150
AdGuard DNS: 94.140.14.14 94.140.15.15
```

Важно: названия сервисов и нумерация DNS-серверов в config.ini должны соответствовать тем, что указаны в файлах `platformdb` и `dnsdb`.

- Формат файла с доменными именами: по одному домену на строку.
Пример:
```
ab.chatgpt.com
api.openai.com
arena.openai.com
```
Указание URL вместо доменного имени (например, `ab.chatgpt.com/login` вместо `ab.chatgpt.com`) приведет к ошибке.
</details>


<details>
  <summary>Запуск скрипта с файлом конфигурации, отличным от `config.ini` (нажать, чтобы открыть)</summary>

- Указать путь к другому конфигурационному файлу при запуске скрипта можно с помощью опции `-c` (или `--config`). Если параметр не указан, по умолчанию будет использоваться файл `config.ini`.

Пример использования: `main.py -c myconfig.ini`, `python main.py -c config2.ini` или `main.py -c srv5.ini` и т.д.
</details>


<details>
  <summary>Личный (локальный) список с доменными именами (нажать, чтобы открыть)</summary>

- Создайте файл `custom-dns-list.txt`, запишите в него доменные имена и разместите его рядом со скриптом. Список будет автоматически подхвачен при запуске и появится в меню как "Custom DNS list".

- Пример файла `custom-dns-list.txt`:
```
ab.chatgpt.com
api.openai.com
arena.openai.com
```
Указание URL вместо доменного имени (например, `ab.chatgpt.com/login` вместо `ab.chatgpt.com`) приведет к ошибке.
</details>


<details>
  <summary>Запуск в Docker (нажать, чтобы открыть)</summary>

```
curl -L -s "https://raw.githubusercontent.com/Ground-Zerro/DomainMapper/refs/heads/main/dm-docker.sh" > /tmp/dm-docker.sh && chmod +x /tmp/dm-docker.sh && sh /tmp/dm-docker.sh
```
</details>


<details>
  <summary>Для пользователей Windows (нажать, чтобы открыть)</summary>

- Загляните в директорию [Windows](https://github.com/Ground-Zerro/DomainMapper/tree/main/Windows) репозитория.
</details>


---

### Генерация всех маршрутов Keenetic одной командой

Из корня проекта, с отключённым VPN ноутбука:

```bash
.venv/bin/python main.py -c keen-config.ini
```

Цепочка задана параметрами `run` в конфигурациях:

1. `keen-config.ini`: общий набор сервисов, результат `domain-ip-resolve.txt`.
2. `keen-custom.ini`: пользовательские домены, результат `domain-ip-custom.txt`.
3. `keen-youtube.ini`: YouTube, результат `domain-ip-youtube.txt`.
4. `keen-openai.ini`: OpenAI и ChatGPT, результат `domain-ip-openai.txt`.
5. `merge_routes.py`: объединение четырёх результатов в `merged-routes.txt`.

`config.ini` дублирует первый профиль, поэтому `.venv/bin/python main.py`
запускает ту же цепочку. `config-old.ini` является старой конфигурацией и в неё не входит.
Дочерние команды используют то же окружение Python. При ошибке команды, некорректной
конфигурации или отсутствии всех IP-адресов на этапе цепочка завершается с ненулевым кодом.
Старый итоговый файл может остаться на диске; при ошибке он не считается новым результатом.
Отдельные ошибки DNS для доменов не останавливают генерацию, смотрите статистику каждого этапа.
Одновременно выполняется не более 40 DNS-запросов суммарно по всем сервисам и серверам.

Итог содержит команды Keenetic через `Wireguard1`. Сначала генерируются точечные `/32`,
затем удаляются дубли и объединяются полностью покрытые смежные сети без добавления
посторонних адресов. Для другого VPN измените `keenetic` во всех четырёх профилях.
Команды из итогового файла нужно применить на роутере отдельно.

Профили используют локальные `platformdb` и `dnsdb`. OpenAI берётся из
`platforms/dns-openai.txt`; системный DNS и Google/Cloudflare выбираются номерами `1 2 4`.
Все четыре профиля используют системный DNS и Google/Cloudflare (`1 2 4`). Cloudflare не исключается.
Генератор отправляет обычные DNS-запросы и сам не защищает от их перехвата.
Статические маршруты требуют обновления при смене адресов; IPv6 этим профилем не покрывается.
Официальный список доменов: [сетевые рекомендации OpenAI](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps).

### Утилита объединения маршрутов `merge_routes.py`

Объединяет файлы маршрутов Keenetic: удаляет дубли, покрытые подсети и сворачивает смежные сети без расширения набора адресов.

**Использование:**

```bash
python merge_routes.py domain-ip-custom.txt domain-ip-youtube.txt domain-ip-resolve.txt -o merged-routes.txt
```

По умолчанию результат сохраняется в `merged-routes.txt`. Чтобы указать другой файл:

```bash
python merge_routes.py file1.txt file2.txt -o result.txt
```

**Примеры:**

```bash
# Объединить три файла, результат в merged-routes.txt
python merge_routes.py domain-ip-custom.txt domain-ip-youtube.txt domain-ip-resolve.txt

# Объединить два файла, указать имя выходного файла
python merge_routes.py domain-ip-youtube.txt domain-ip-resolve.txt -o routes-combined.txt
```

**Логика обработки:**
- Точные дубли убираются.
- Если одна сеть является подсетью другой (например, `192.168.1.0/24` входит в `192.168.0.0/16`), в результат попадает только более крупная (`/16`).
- Смежные сети объединяются только при полном покрытии: два соседних `/32` могут стать `/31`.
- Разные интерфейсы, параметры маршрута и семейства IP обрабатываются отдельно.
- Комментарии объединяемых сетей собираются вместе; у точного дубля сохраняется первый комментарий.
- Если входной файл отсутствует или не содержит маршрутов, команда завершается с ошибкой до записи результата.

---

# ☕ Поддержка

Если проект оказался Вам полезен — можно поблагодарить автора:

- [Поддержать на Boosty](https://boosty.to/ground_zerro)
