#!/usr/bin/env bash

extract_title() {
    echo "$1" | jq -r '.talk.title'
}

extract_type() {
    echo "$1" | jq -r '.talk.talkType'
}

extract_espaced_title() {
    title=$(echo "$1" | jq -r '.talk.title')
    echo "$title" | tr -d ":\"'," | sed "s/ /-/g"
}

extract_speakers() {
    echo "$1" | jq -r '.talk.speakers[] | ("link:" + .link.href + "[" + .name + "]")'
}

extract_summary() {
    echo "$1" | jq -r '.talk.summary'
}

extract_id() {
    echo "$1" | jq -r '.talk.id'
}

generate_file() {
    path=$1
    title=$2
    type=$3
    speakers=$4
    summary=$5

    cat <<EOF >"$path.adoc"
== $title

> $type

$speakers


== Abstract

$summary

== Mes notes

TODO
EOF
}

process_day() {
    file=$1
    favoriteTalks=$2
    folder=$3
    # TODO Check jq errors
    jq -c '.slots[]' "$file" | while read i; do
        # echo $i | jq
        id=$(extract_id "$i")
        if [[ $favoriteTalks == *$id* ]]; then
            echo "$id"
            echo "DEBUG : $i"
            # TODO test if file exists
            generate_file "$folder/$(extract_espaced_title "$i")" "$(extract_title "$i")" "$(extract_type "$i")" "$(extract_speakers "$i")" "$(extract_summary "$i")"
            echo "---"
        fi
    done
}

# wed thu fri
day=$1

# TODO Get favorites
#favoriteTalks="GNA-8922 GNA-8924"
favoriteTalks=$2

if [[ $day == "wed" ]]; then
    curl -H "Accept: application/json" https://cfp.devoxx.fr/api/conferences/DevoxxFR2023/schedules/wednesday -o talks.json
    mkdir -p mercredi
    process_day talks.json "$favoriteTalks" mercredi
fi

if [[ $day == "thu" ]]; then

    curl -H "Accept: application/json" https://cfp.devoxx.fr/api/conferences/DevoxxFR2023/schedules/thursday -o talks.json
    mkdir -p jeudi
    process_day talks.json "$favoriteTalks" jeudi
fi

if [[ $day == "fri" ]]; then
    curl -H "Accept: application/json" https://cfp.devoxx.fr/api/conferences/DevoxxFR2023/schedules/friday -o talks.json
    mkdir -p vendredi
    process_day talks.json "$favoriteTalks" vendredi
fi

# FIXME missing condition
find . -name '.adoc' -delete
