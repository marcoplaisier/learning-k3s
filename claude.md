# Project Instructions

## Project Overview
This is a K3s learning project with various application deployments and monitoring stack.

## Working with Manifests

### Conventions
- Keep manifests organized by application in `manifests/apps/`
- Each application should have its own directory
- Common resources: `namespace.yaml`, `deployment.yaml`, `service.yaml`, `ingress.yaml`
- Follow consistent naming patterns across all manifests

### Before Applying Changes
- Validate YAML syntax before applying
- Use `kubectl apply --dry-run=client` to verify manifests
- Check for proper indentation and structure
- Ensure namespace exists before creating resources in it

### Testing Changes
- Test manifest changes with: `kubectl apply --dry-run=client -f <file>`
- Validate with: `kubectl apply --dry-run=server -f <file>`
- Use `kubectl diff -f <file>` to see what would change
- After applying, verify with: `kubectl get all -n <namespace>`

## Git Workflow
- Work from feature branches for new functionality
- Commit after completing logical units of work
- Write clear, descriptive commit messages
- Review changes with `git diff` before committing

## Common Commands
```bash
# Validate Kubernetes manifests
kubectl apply --dry-run=client -f manifests/

# Check cluster resources
kubectl get all --all-namespaces

# View logs
kubectl logs -n <namespace> <pod-name>

# Describe resources
kubectl describe <resource-type> <name> -n <namespace>
```

## Applications in this Project
- Argo CD - GitOps continuous delivery tool
- Flame Dashboard - Application dashboard
- Image Processor - Image processing service
- Kube Prometheus Stack - Monitoring and alerting
- Traefik - Ingress controller

## Notes
- Always verify namespace exists before creating resources
- Check ingress configurations for proper routing
- Ensure services match deployment selectors
- Verify resource limits and requests are set appropriately