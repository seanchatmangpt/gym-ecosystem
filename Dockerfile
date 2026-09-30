ARG GGEN_ECOSYSTEM_IMAGE=ghcr.io/seanchatmangpt/ggen-ecosystem:latest
FROM ${GGEN_ECOSYSTEM_IMAGE}

ARG SOURCE_SHA=unknown
ARG RELEASE_VERSION=26.9.30
LABEL org.opencontainers.image.source="https://github.com/seanchatmangpt/gym-ecosystem" \
      org.opencontainers.image.revision="${SOURCE_SHA}" \
      org.opencontainers.image.version="${RELEASE_VERSION}" \
      org.opencontainers.image.description="Pinned gym reference corpus + AutoFDE/GymAct/beam4pm control plane on the ggen manufacturer runtime"

WORKDIR /opt/gym-ecosystem
COPY .gitmodules ecosystem.lock.toml README.md VERSION ./
COPY scripts ./scripts
COPY vendor ./vendor

RUN chmod +x scripts/*.sh \
 && ./scripts/container-smoke.sh

CMD ["bash", "-lc", "./scripts/container-smoke.sh"]
