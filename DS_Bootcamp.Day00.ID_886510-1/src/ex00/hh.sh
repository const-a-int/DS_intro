#!/bin/sh

VACANCY=$"Data Scientist"
curl --get --silent "https://api.hh.ru/vacancies" --data-urlencode "text=${VACANCY}" --data "per_page=20" --data "page=0" | jq '.' > hh.json