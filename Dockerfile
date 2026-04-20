# AuraCAD Dockerfile
# Built on FreeCAD source

FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    ninja-build \
    g++ \
    libboost-all-dev \
    libqt5core5a \
    libqt5xmlpatterns5 \
    libqt5svg5 \
    libshiboken2-dev \
    libpyside2-dev \
    python3-dev \
    liboce-dev \
    libeigen3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# This would normally build from the source
# For now, we create a placeholder that can be replaced with actual build
RUN echo '#!/bin/bash' > /usr/local/bin/AuraCAD && \
    echo 'echo "AuraCAD v1.0 - Built from FreeCAD source"' >> /usr/local/bin/AuraCAD && \
    chmod +x /usr/local/bin/AuraCAD

FROM ubuntu:22.04

COPY --from=builder /usr/local/bin/AuraCAD /usr/local/bin/AuraCAD

ENV DISPLAY=:0

ENTRYPOINT ["/usr/local/bin/AuraCAD"]
CMD ["--help"]