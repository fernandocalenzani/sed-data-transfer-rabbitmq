#!/bin/sh

echo "-----------------------------------"
echo "| PROJECT       | MIMIR            |"
echo "| VERSION       | 0.1.0            |"
echo "| COMPANY       | ARISE TECHNOLOGY |"
echo "-----------------------------------"
echo ""

#________________________________________________________________
# PRE-BUILD
#________________________________________________________________
echo "[MIMIR] Starting pre-build..."

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

  ./project/firmware/consumer/packages
  ./project/firmware/producer/packages
  ./project/backend/packages
  ./project/ai/packages
  ./project/frontend/packages
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
echo "[MIMIR] Pre-build concludes successfully"
echo ""
echo "[MIMIR] starting docker"

docker-compose up --build
