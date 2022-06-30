ARG PY_VER
ARG DIST
ARG IMAGE
ARG PKG_NAME
ARG PKG_VERSION

FROM datajoint/${IMAGE}:py${PY_VER}-${DIST}
COPY --chown=anaconda:anaconda ./requirements.txt ./setup.py \
    /main/
COPY --chown=anaconda:anaconda ./${PKG_NAME} /main/${PKG_NAME}
RUN \
    cd /main && \
    pip install . && \
    rm -R /main/*
WORKDIR /main