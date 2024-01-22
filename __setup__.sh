#!/bin/sh

#________________________________________________________________
# PRE-BUILD
#________________________________________________________________

SRC_FOLDERS=(
  ./setup/secrets/.env
  ./setup/secrets/.env
  ./setup/secrets/.env

  ./setup/config
  ./setup/config
  ./setup/config
  ./setup/config
)

DEST_FOLDERS=(
  ./project/firmware/.env
  ./project/ai/.env
  ./project/backend/.env

  ./project/firmware/config
  ./project/ai/config
  ./project/backend/config
  ./project/frontend/config
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
