# ---|DOCKERFILE|---


# |---|BUILDER PIPE|----------------------------|

#............................
# ---|BUILDER PIPE|---
FROM python:3.10 AS PIPE

WORKDIR /mimir/pipe

#............................
# ---|LIBRARIES|---
COPY pipe/requirements.txt ./

#............................
# ---|UPDATE PACKAGES|---
RUN apt-get update && \
    apt-get install -y curl

RUN python -m pip install --upgrade pip

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r ./requirements.txt

#............................
# ---|OTHERS FILES|---
COPY pipe/consumer ./consumer/
COPY pipe/producer ./producer/
COPY pipe/ai ./ai/
COPY pipe/ ./

#............................
# ---|CMD|---
