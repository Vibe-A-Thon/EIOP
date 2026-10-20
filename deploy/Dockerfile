FROM python:3.11.14-slim-bookworm AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/opt/eoip:/opt/eoip/packages
RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/eoip
COPY requirements.lock requirements-fileparse.lock requirements-numerics.lock ./
RUN pip install --no-cache-dir -r requirements.lock -r requirements-fileparse.lock
# FT-X03: numpy/scipy/scikit-learn are imported at API startup (processing router).
RUN pip install --no-cache-dir --require-hashes --no-deps -r requirements-numerics.lock
COPY pyproject.toml ./
COPY LICENSE NOTICE LICENSING.md THIRD_PARTY_NOTICES.md ./
COPY licenses ./licenses
COPY packages ./packages
RUN pip install --no-cache-dir --no-deps .
COPY apps ./apps
COPY config ./config
COPY demo ./demo
COPY schemas ./schemas
COPY scripts ./scripts
COPY EOIP-engg-doc-pkg/gaps-requirements.md EOIP-engg-doc-pkg/gaps-implementation.md EOIP-engg-doc-pkg/gaps2-requirements.md EOIP-engg-doc-pkg/gaps2-implementation.md ./EOIP-engg-doc-pkg/
RUN git -C demo/demodata/core/demo-repo init -b main && \
    git -C demo/demodata/core/demo-repo add . && \
    GIT_AUTHOR_DATE=2026-10-01T00:00:00Z GIT_COMMITTER_DATE=2026-10-01T00:00:00Z \
    git -C demo/demodata/core/demo-repo -c user.name='EOIP Demo' -c user.email=demo@example.invalid commit -m 'EOIP-1 implement impact calculation; EOIP-2 retain evidence' && \
    useradd --uid 10001 --create-home eoip && mkdir -p /data && chown -R eoip:eoip /data /opt/eoip
USER eoip
# FT-AUTH: provision only what the operator configured (EOIP_ADMIN_USERNAME +
# EOIP_ADMIN_PASSWORD(_FILE); EOIP_API_TOKEN + EOIP_API_TOKEN_ROLES), then serve.
# There is no default account; without any principal the API refuses to start.
CMD ["sh", "-c", "python -m eoip.authn.provision from-env && exec python -m uvicorn apps.api.main:create_app --factory --host 0.0.0.0 --port 8000"]

FROM runtime AS test
USER root
RUN pip install --no-cache-dir -c requirements.lock '.[test]'
COPY tests ./tests
# FT-X11: acceptance reports go to a named volume at /results; a fresh named volume
# inherits this owner, so uid 10001 can write without a world-writable bind mount.
RUN mkdir -p /results && chown eoip:eoip /results
USER eoip
CMD ["python", "-m", "pytest", "-q"]
