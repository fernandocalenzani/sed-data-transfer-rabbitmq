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
  ./project/backend/app/.env
  ./project/ai/.env

  ./project/firmware/consumer/config
  ./project/firmware/producer/config
  ./project/backend/app/src/config
  ./project/ai/config
  ./project/frontend/config

  ./project/firmware/consumer/packages
  ./project/firmware/producer/packages
  ./project/backend/app/src/packages
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

#!/bin/bash

# Defina as variáveis padrão
REMOVE_VOLUMES=false
REMOVE_CONTAINERS=false

# Processa as opções de linha de comando
while getopts ":rmv" opt; do
  case $opt in
    r)
      REMOVE_VOLUMES=true
      REMOVE_CONTAINERS=true
      ;;
    m)
      REMOVE_VOLUMES=true
      ;;
    v)
      REMOVE_VOLUMES=true
      ;;
    \?)
      echo "Opção inválida: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Verifica as opções fornecidas e executa os comandos correspondentes
if [ "$REMOVE_VOLUMES" = true ]; then
  echo "[MIMIR] removing volumes"
  docker volume prune --force
fi

if [ "$REMOVE_CONTAINERS" = true ]; then
  echo "[MIMIR] removing containers"
  docker-compose down -v --rmi all
fi

# Inicia os contêineres após remover, se necessário
docker-compose up --build -d --quiet-pull
