# Deployment

The Hybrid Routing API V4 (`api_hybrid_v4.py`) ships as a Docker image built
on `gcr.io/distroless/python3-debian13:nonroot`. The image has no shell or
package manager, and the app runs as a non-root user.

## Requirements

| Item | Minimum |
| --- | --- |
| Docker | 23+ with BuildKit (default since Docker 23) |
| RAM | 5 GB for the container (about 4.1 GB in use once the graph is loaded) |
| Disk | About 1 GB for the image |
| Git LFS | Needed to get the road graph (see below) |

## The road graph and Git LFS

`graphsv2/truck_network_realistic.graphml` (about 350 MB) is stored in Git LFS.
A clone without LFS contains only a small text pointer in its place, and the
API cannot start from that.

The build handles both cases:

- **The checkout has the real file**: the build copies it in as-is.
- **The checkout has only the pointer**: the build clones the repo, runs
  `git lfs pull`, and checks the file's sha256 against the pointer. The build
  fails if they don't match.

To get the real file locally:

```bash
git lfs install
git lfs pull
```

Check that the file is about 350 MB and not about 130 bytes:

```bash
ls -lh graphsv2/truck_network_realistic.graphml
```

## Build

### Option A: the local checkout has the LFS file

```bash
docker build -t hybrid-routing:v4 .
```

### Option B: the checkout has only the pointer (CI, or a clone without LFS)

The repository is private, so the build needs a GitHub token to fetch the graph.
Pass the token as a BuildKit secret, which keeps it out of the image layers and
history:

```bash
GH_TOKEN=$(gh auth token) \
  docker build --secret id=gh_token,env=GH_TOKEN -t hybrid-routing:v4 .
```

Any token with read access to the repo works, such as a fine-grained PAT with
`Contents: Read`, or `GITHUB_TOKEN` in GitHub Actions.

### Build arguments

| Arg | Default | Purpose |
| --- | --- | --- |
| `REPO_URL` | `https://github.com/Reynadi531/v4-multi-vehicle-routing.git` | Repo to fetch the LFS file from |
| `GIT_REF` | `main` | Branch or tag to fetch from. The fetched file must match the pointer in your checkout |
| `GRAPH_PATH` | `graphsv2/truck_network_realistic.graphml` | Path to the LFS graph |

If you build an older commit from a pointer-only checkout, set `GIT_REF` to a
branch or tag that has the same graph. Otherwise the sha256 check fails.

## Run

```bash
docker run -d --name hybrid-routing \
  -p 8000:8000 \
  --memory 5g \
  --restart unless-stopped \
  hybrid-routing:v4
```

The graph loads at startup, which takes about 30 to 60 seconds. Until it
finishes, the port refuses connections. To follow progress:

```bash
docker logs -f hybrid-routing
```

The image has a built-in `HEALTHCHECK` with a 120 s start period. Check it with:

```bash
docker inspect -f '{{.State.Health.Status}}' hybrid-routing
```

### Docker Compose

```yaml
services:
  hybrid-routing:
    build: .
    image: hybrid-routing:v4
    ports:
      - "8000:8000"
    mem_limit: 5g
    restart: unless-stopped
```

To build from a pointer-only checkout with Compose, add the secret:

```yaml
services:
  hybrid-routing:
    build:
      context: .
      secrets:
        - gh_token
    # ...

secrets:
  gh_token:
    environment: GH_TOKEN
```

## Workers and scaling

Run **one uvicorn worker per container**. Each worker loads its own copy of the
graph, which adds about 4 GB of RAM. To handle more traffic, run more containers
behind a load balancer.

To change uvicorn flags, override `CMD`. `ENTRYPOINT` already runs
`python -m uvicorn api_hybrid_v4:app`:

```bash
docker run -p 9000:9000 hybrid-routing:v4 --host 0.0.0.0 --port 9000 --workers 1
```

## Health checks on other platforms

The image has no shell, so `curl`, `wget`, and `sh -c` are not available. Any
command-style probe has to call Python directly, in exec form:

```json
["/venv/bin/python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=5)"]
```

For HTTP probes (Kubernetes, Cloud Run, ECS target groups), use `GET /` on port
8000 and allow a startup period of at least 120 s.

## Endpoints

All responses use the `medium` vehicle profile and contain four time scenarios:
`early_morning` (03:00), `morning` (09:00), `afternoon` (15:00), and `night` (21:00).

### `GET /`

Status check.

```bash
curl http://localhost:8000/
```

### `GET /route/v1/driving/{lon1},{lat1};{lon2},{lat2}`

OSRM-style path. Coordinates are **longitude first**.

```bash
curl 'http://localhost:8000/route/v1/driving/106.8456,-6.2088;106.6297,-6.1781'
```

### `POST /route`

```bash
curl -X POST http://localhost:8000/route \
  -H 'Content-Type: application/json' \
  -d '{"origin_lat": -6.2088, "origin_lon": 106.8456,
       "destination_lat": -6.1781, "destination_lon": 106.6297}'
```

The interactive API docs are at `http://localhost:8000/docs`.

## Updating

1. `git pull`, then `git lfs pull` if the graph changed.
2. Rebuild: `docker build -t hybrid-routing:v4 .`
3. Replace the container: `docker rm -f hybrid-routing`, then run it again.

Pip dependencies are cached in their own build stage, so a rebuild reinstalls
them only when `requirements.txt` changes.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Build fails with `cannot clone ... Private repo?` | Pointer-only checkout with no token | Use Option B, or run `git lfs pull` locally first |
| Build fails with `sha256 ... does not match pointer` | `GIT_REF` points to a different graph version | Set `--build-arg GIT_REF=<branch or tag>` to one that matches your checkout |
| Container exits or restarts during startup | Out of memory while loading the graph | Give the container at least 5 GB (`--memory 5g`) |
| `Connection refused` right after start | Graph is still loading | Wait 30 to 60 s, or watch `docker logs -f` |
| Health status stays `starting` | A shell-form health check was configured on the platform | Use the exec-form Python command shown above |
| Every scenario returns an `error` field | Coordinates are outside the graph area, or lat/lon are swapped | The GET path expects `lon,lat`. The POST body uses named fields |
