#!/bin/sh

year=2023
play_session=
declare -a days=("wed" "thu" "fri")

for day in "${days[@]}"
do
  url="https://cfp.devoxx.fr/${year}/byday/${day}"

  curl ${url} -s \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
    -H 'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6' \
    -H 'Cache-Control: no-cache' \
    -H 'Connection: keep-alive' \
    -H "Cookie: PLAY_SESSION=${play_session}" \
    -H 'Pragma: no-cache' \
    -H "Referer: ${url}" \
    -H 'Sec-Fetch-Dest: document' \
    -H 'Sec-Fetch-Mode: navigate' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-User: ?1' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
    -H 'sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "macOS"' \
    --compressed > ${day}.json

  fav_ids=$(node ./parse_fav.js ${day})

  ./favs2adoc.sh ${day} ${fav_ids}

  rm -rf ${day}.json
done
