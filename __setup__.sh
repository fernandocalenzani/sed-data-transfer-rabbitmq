#!/bin/sh

#________________________________________________________________
# PRE-BUILD
#________________________________________________________________

SRC_FOLDERS=(
  ./setup/secrets/.env
  ./setup/secrets/.env
  ./setup/secrets/.env
  ./setup/secrets/.env

  ./setup/config
  ./setup/config
  ./setup/config
  ./setup/config
  ./setup/config

  ./setup/libs/firmware
  ./setup/libs/firmware
  ./setup/libs/backend
  ./setup/libs/ai
  ./setup/libs/frontend
)

DEST_FOLDERS=(
  ./project/firmware/consumer/.env
  ./project/firmware/producer/.env
  ./project/backend/.env
  ./project/ai/.env

  ./project/firmware/consumer/config
  ./project/firmware/producer/config
  ./project/backend/config
  ./project/ai/config
  ./project/frontend/config

  ./project/firmware/consumer/libs
  ./project/firmware/producer/libs
  ./project/backend/libs
  ./project/ai/libs
  ./project/frontend/libs
)

remove_directories() {
  if [ -d "$1" ]; then
    rm -rf "$1"
  fi
}

# Remover diretórios de destino
for dir in "${DEST_FOLDERS[@]}"; do
  remove_directories "$dir"
done

i=0
while [ $i -lt ${#SRC_FOLDERS[@]} ]; do
  src_dir="${SRC_FOLDERS[$i]}"
  dest_dir="${DEST_FOLDERS[$i]}"
  cp -r "$src_dir" "$dest_dir"
  i=$((i + 1))
done

#________________________________________________________________
# Docker
#________________________________________________________________
docker-compose up --build
