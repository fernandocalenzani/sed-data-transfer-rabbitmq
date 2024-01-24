#________________________________________________________________
# DOCKERFILE

#________________________________________________________________
# BUILDER
#________________________________________________________________
FROM python:3.10 AS builder

WORKDIR /mimir/

COPY project/consumer/requirements.txt ./consumer/
COPY project/producer/requirements.txt ./producer/
COPY project/ai/requirements.txt ./ai/

# Install dependencies
RUN apt-get update && \
  apt-get install -y curl

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

RUN apt-get update && \
  apt-get upgrade -y && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
  apt-get install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r ./consumer/requirements.txt && \
  pip install --no-cache-dir -r ./producer/requirements.txt && \
  pip install --no-cache-dir -r ./ai/requirements.txt

# env
COPY setup/secrets/.env ./consumer/
COPY setup/secrets/.env ./producer/
COPY setup/secrets/.env ./ai/

# Dependencies
COPY setup/config ./consumer/config
COPY setup/config ./producer/config
COPY setup/config ./ai/config

# Dependencies
COPY setup/libs/consumer_producer ./consumer/packages
COPY setup/libs/consumer_producer ./producer/packages
COPY setup/libs/ai ./ai/packages

# Copy the entire project
COPY project/consumer ./consumer/
COPY project/producer ./producer/
COPY project/ai ./ai/

#________________________________________________________________
# CMD
#________________________________________________________________
FROM builder

WORKDIR /mimir

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

CMD ["docker-entrypoint.sh"]
