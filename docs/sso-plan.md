# Single sign-on for the homelab

Status: plan, not started (2026-10-01).

Goal: one login for every service on the cluster, managed as Argo CD apps in
this repo like everything else.

## Shape

One identity provider speaking OpenID Connect, plus a forward-auth gate in
Traefik for apps that cannot do OIDC themselves.

## Steps, in order

### 1. HTTPS everywhere (prerequisite)

OIDC redirects and session cookies need TLS. Deploy cert-manager with one of:

- an internal CA, trusted on all devices (simplest, fully offline), or
- Let's Encrypt via DNS-01 if a real domain is available and the
  `*.homelab.internal` names move under it.

Useful on its own regardless of SSO, and the largest piece of groundwork.

### 2. Identity provider: Authentik

Best fit for this cluster:

- OIDC provider for apps that support it.
- Embedded outpost that plugs into Traefik `ForwardAuth` for apps that do not.
- Needs PostgreSQL and Redis. Use a `bulk` PVC for Postgres, pinned to the
  controlplane (its /mnt/bulk is the SSD; worker-1's is the HDD).

Alternatives considered:

- Keycloak: heavier, no forward-auth of its own.
- Pocket ID: lightweight passkey-only OIDC, but no forward-auth.

### 3. Native OIDC integrations (highest payoff first)

| App     | Mechanism                                   | Notes                                  |
|---------|---------------------------------------------|----------------------------------------|
| Argo CD | `oidc.config` in `argocd-cm`                | group-based RBAC in `argocd-rbac-cm`   |
| Gitea   | OpenID Connect authentication source        | enable auto-registration               |
| Grafana | generic OAuth                               | map groups to Admin / Editor / Viewer  |

Each is a config change plus a client registration in Authentik.

### 4. Forward-auth for the rest

Flame dashboard, Traefik dashboard, Prometheus, Alertmanager: one Traefik
middleware pointing at the Authentik outpost, attached to their ingresses.

### 5. Django inventory app

- Quick: put it behind forward-auth and enable `RemoteUserMiddleware` so
  accounts are created from the header Authentik passes through.
- Proper: an OIDC client such as `mozilla-django-oidc` for real logout and
  group sync.

### 6. Karavan

Supports OIDC through its own configuration; do last.

## Secrets

Client secrets must not live in the repo in plain form. Add sealed-secrets or
SOPS as part of this work.

## First concrete step

cert-manager with an internal CA.
