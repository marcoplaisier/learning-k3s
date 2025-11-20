# Application Manifests - Patterns and Conventions

This directory contains Kubernetes manifests for deploying applications to the k3s cluster. The manifests follow specific patterns to ensure maintainability, proper deployment ordering, and GitOps compatibility.

## Directory Structure

Each application has its own subdirectory containing individual manifest files:

```
manifests/apps/
├── inventory/
│   ├── namespace.yaml
│   ├── service.yaml
│   ├── deployment.yaml
│   └── ingress.yaml
├── karavan/
│   ├── namespace.yaml
│   ├── serviceaccount.yaml
│   ├── deployment.yaml
│   └── ...
└── ...
```

## Key Patterns

### Small, Focused Files

**Pattern**: One Kubernetes resource per file, with descriptive filenames.

**Rationale**:
- **Git-friendly**: Easier to track changes, review diffs, and understand history
- **Maintainability**: Clear what each file does without opening it
- **Selective application**: Can apply/delete individual resources as needed
- **Reduced conflicts**: Multiple people can work on different resources simultaneously

**Example**: Instead of `app.yaml` with all resources, use:
- `namespace.yaml`
- `serviceaccount.yaml`
- `deployment.yaml`
- `service.yaml`
- `ingress.yaml`

### ArgoCD Sync Waves

**Pattern**: All resources include `argocd.argoproj.io/sync-wave` annotations with numeric values.

**Purpose**: Controls the order in which ArgoCD deploys resources, ensuring dependencies are met.

**Wave Order**:
1. **Wave 1**: Namespaces
2. **Wave 2**: RBAC (ServiceAccounts, Roles, RoleBindings), ConfigMaps, Secrets
3. **Wave 3**: Deployments, StatefulSets, DaemonSets, **and their PVCs**
4. **Wave 4**: Services
5. **Wave 5**: Ingresses

**Important**: PersistentVolumeClaims must be in the **same wave** as the Deployment/StatefulSet that uses them. Placing PVCs in an earlier wave can cause a deadlock where the PVC waits for a pod to claim it, but the pod (in a later wave) waits for the earlier wave to complete.

**Example**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: karavan
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

**Benefits**:
- Namespaces exist before resources are created in them
- RBAC and configuration (Secrets/ConfigMaps) are ready before workloads start
- PVCs are created alongside their consuming workloads (avoiding deadlocks)
- Services exist before ingress routes to them
- Predictable, repeatable deployments

### Naming Conventions

- **Files**: Lowercase, descriptive (e.g., `postgres-deployment.yaml`, `servicemonitor.yaml`)
- **Resources**: Application name prefixed where appropriate (e.g., `karavan-service`, `inventory-ingress`)
- **Namespaces**: Generally match the application name

### Standard Resource Configuration

**Services**:
- Type: `ClusterIP` (default)
- Port: 80 (frontend) or application-specific
- Selector: Matches deployment labels

**Ingresses**:
- Host-based routing with `.local` domain for development
- Path: `/` with `Prefix` pathType
- Sync wave: 5 (after services)

**Deployments**:
- Include health checks (livenessProbe, readinessProbe) where applicable
- Use specific container ports (e.g., 8080, 8000)
- Environment configuration via ConfigMaps or Secrets
- Sync wave: 3

## Adding New Applications

When adding a new application:

1. Create a new subdirectory: `manifests/apps/<app-name>/`
2. Create individual manifest files for each resource
3. Add sync-wave annotations to all resources
4. Follow the naming conventions
5. Include health checks in deployments
6. Use ConfigMaps/Secrets for configuration

## ArgoCD Integration

These manifests are designed to be consumed by ArgoCD Applications. The sync waves ensure proper ordering, and the small file structure makes it easy to see what changed between Git commits.
