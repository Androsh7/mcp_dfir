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
&& rm -rf /var/lib/apt/lists/*

# Install python tools
RUN pip install --upgrade pip setuptools wheel \
&& git clone https://github.com/volatilityfoundation/volatility3.git \
&& cd volatility3 \
&& pip install -e ".[full]" \
# Create aliases for vol.py and pdbconv.py
&& printf '#!/bin/bash\npython3 /tools/volatility3/vol.py "$@"\n' > /usr/local/bin/vol \
&& chmod +x /usr/local/bin/vol \
&& printf '#!/bin/bash\npython3 /tools/volatility3/volatility3/framework/symbols/windows/pdbconv.py "$@"\n' > /usr/local/bin/pdbconv \
&& chmod +x /usr/local/bin/pdbconv

# Create analyst user
RUN useradd -m -d /analysis analyst \
&& chown -R analyst:analyst /tools
USER analyst

ENTRYPOINT ["sleep", "infinity"]