FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VOLATILITY_SYMBOLS=/usr/local/lib/python3.12/site-packages/volatility3/symbols


WORKDIR /tools

# Install libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    sleuthkit \
    git \
    curl \
    unzip \
&& rm -rf /var/lib/apt/lists/*

# Install python tools
RUN pip install --upgrade pip setuptools wheel \
&& pip install volatility3

# Install windows symbols
# RUN curl -fsSL https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip -o windows.zip \
# && unzip windows.zip \
# && mv windows ${VOLATILITY_SYMBOLS}/ \
# && rm windows.zip

# Install linux symbols
# RUN curl -fsSL https://github.com/Abyss-W4tcher/volatility3-symbols/archive/refs/heads/master.zip -o master.zip \
# && unzip master.zip \
# && mkdir -p ${VOLATILITY_SYMBOLS}/linux \
# && find volatility3-symbols-master -name "*.json.xz" -exec mv {} ${VOLATILITY_SYMBOLS}/linux/ \; \
# && rm -rf master.zip volatility3-symbols-master

# Create analyst user
RUN useradd -m -d /analysis analyst \
&& chown -R analyst:analyst /usr/local/lib/python3.12/site-packages/volatility3/
USER analyst

ENTRYPOINT ["sleep", "infinity"]