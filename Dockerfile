# ---|DOCKERFILE|---

#................................................................
# ---|BUILDER|---
#................................................................
FROM python:3.10 AS builder

WORKDIR /mimir/

#................................................................
# ---|ENV|---
#................................................................
ENV RABBIT_USERNAME="admin"
ENV RABBIT_PASSWORD="admin"
ENV MONGO_HOST = "mongodb+srv://admin:TTH2kszKqxF0AHpu@arise-lab.tcfidx2.mongodb.net/db-mimir?retryWrites=true&w=majority"
ENV MONGO_DB = "db-mimir"
ENV DEVICE = "mimir"

#................................................................
# ---|INSTALLATION|---
#................................................................
COPY project/consumer/requirements.txt ./consumer/
COPY project/producer/requirements.txt ./producer/
COPY project/ai/requirements.txt ./ai/

RUN apt-get update && \
  apt-get install -y curl

RUN python -m pip install --upgrade pip

RUN apt-get update && \
  apt-get upgrade -y && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
  apt-get install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r ./consumer/requirements.txt && \
  pip install --no-cache-dir -r ./producer/requirements.txt && \
  pip install --no-cache-dir -r ./ai/requirements.txt


#................................................................
# ---|DEPENDENCIES|---
#................................................................
COPY setup/config ./consumer/config
COPY setup/config ./producer/config
COPY setup/config ./ai/config

COPY setup/libs/consumer_producer ./consumer/packages
COPY setup/libs/consumer_producer ./producer/packages
COPY setup/libs/ai ./ai/packages

#................................................................
# ---|OTHERS FILES|---
#................................................................
COPY project/consumer ./consumer/
COPY project/producer ./producer/
COPY project/ai ./ai/

#................................................................
# ---|CMD|---
#................................................................
FROM builder

WORKDIR /mimir

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

CMD ["docker-entrypoint.sh"]
