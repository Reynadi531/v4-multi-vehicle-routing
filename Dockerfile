# syntax=docker/dockerfile:1.7

# The builder and runtime must share the same Debian release so the venv's
# interpreter (/usr/bin/python3, 3.13) and glibc match the distroless image.
ARG DEBIAN_RELEASE=13

# ==================================================
# Stage 1: Python dependencies
# ==================================================
FROM debian:${DEBIAN_RELEASE}-slim AS deps

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt \
 && find /venv -name '__pycache__' -type d -prune -exec rm -rf {} +

# ==================================================
# Stage 2: application files + Git LFS graph
# ==================================================
FROM debian:${DEBIAN_RELEASE}-slim AS source

ARG REPO_URL=https://github.com/Reynadi531/v4-multi-vehicle-routing.git
ARG GIT_REF=main
ARG GRAPH_PATH=graphsv2/truck_network_realistic.graphml

RUN apt-get update \
 && apt-get install -y --no-install-recommends git git-lfs ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# If the build context only holds the LFS pointer (repo cloned without
# `git lfs pull`), fetch the real graph from the remote and check it against
# the sha256 recorded in the pointer.
# For a private repo, pass a token:
#   docker build --secret id=gh_token,env=GH_TOKEN .
RUN --mount=type=secret,id=gh_token,required=false <<'EOF'
set -eu
if head -c 200 "$GRAPH_PATH" | grep -q '^version https://git-lfs'; then
    echo "LFS pointer found at $GRAPH_PATH, fetching from $REPO_URL ($GIT_REF)"
    expected=$(sed -n 's/^oid sha256://p' "$GRAPH_PATH")
    url="$REPO_URL"
    if [ -s /run/secrets/gh_token ]; then
        url=$(echo "$REPO_URL" | sed "s#https://#https://x-access-token:$(cat /run/secrets/gh_token)@#")
    fi
    export GIT_TERMINAL_PROMPT=0
    if ! GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --branch "$GIT_REF" "$url" /tmp/repo; then
        echo "ERROR: cannot clone $REPO_URL. Private repo? Build with:" >&2
        echo "  GH_TOKEN=\$(gh auth token) docker build --secret id=gh_token,env=GH_TOKEN ." >&2
        exit 1
    fi
    git -C /tmp/repo lfs pull --include "$GRAPH_PATH"
    actual=$(sha256sum "/tmp/repo/$GRAPH_PATH" | cut -d' ' -f1)
    if [ "$actual" != "$expected" ]; then
        echo "ERROR: fetched graph sha256 $actual does not match pointer $expected" >&2
        echo "Run 'git lfs pull' locally, or set GIT_REF to the commit you are building." >&2
        exit 1
    fi
    mv "/tmp/repo/$GRAPH_PATH" "$GRAPH_PATH"
    rm -rf /tmp/repo
fi
if head -c 200 "$GRAPH_PATH" | grep -q '^version https://git-lfs'; then
    echo "ERROR: $GRAPH_PATH is still an LFS pointer" >&2
    exit 1
fi
EOF

# ==================================================
# Stage 3: distroless runtime
# ==================================================
FROM gcr.io/distroless/python3-debian${DEBIAN_RELEASE}:nonroot

COPY --from=deps /venv /venv
COPY --from=source --chown=nonroot:nonroot /app /app

WORKDIR /app

ENV PATH=/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLCONFIGDIR=/tmp

EXPOSE 8000

# Exec form only: distroless has no /bin/sh, so shell-form checks never run.
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD ["/venv/bin/python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=5)"]

# The graph is loaded at import time, so keep a single worker:
# each extra worker loads its own copy of the graph into memory.
ENTRYPOINT ["/venv/bin/python3", "-m", "uvicorn", "api_hybrid_v4:app"]
CMD ["--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
