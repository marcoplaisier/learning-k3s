# K3s Ansible Setup

This directory contains Ansible playbooks to set up a K3s cluster with a control plane and worker nodes.

## Prerequisites

1. **Ansible installed** on your local machine:
   ```bash
   sudo apt update
   sudo apt install ansible
   ```

2. **SSH access** configured to both nodes:
   - Control plane: `192.168.178.81`
   - Worker: `192.168.178.82`

3. **SSH keys** set up for passwordless authentication:
   ```bash
   ssh-copy-id ubuntu@192.168.178.81
   ssh-copy-id ubuntu@192.168.178.82
   ```

4. **Sudo privileges** without password on both nodes (if needed):
   ```bash
   # On each node, add to /etc/sudoers.d/ubuntu
   ubuntu ALL=(ALL) NOPASSWD:ALL
   ```

## Configuration

### Inventory File

The `inventory.ini` file defines the cluster nodes:

```ini
[k3s_control_plane]
controlplane ansible_host=192.168.178.81 ansible_user=ubuntu

[k3s_workers]
worker-1 ansible_host=192.168.178.82 ansible_user=ubuntu
```

**Customize:**
- Update `ansible_user` if you use a different username
- Adjust IP addresses if they change
- Add more workers by adding entries under `[k3s_workers]`

## Usage

### Setup K3s Cluster

Run the main playbook to install and configure the K3s cluster:

```bash
cd ansible
ansible-playbook k3s-setup.yml
```

This playbook will:
1. Install K3s on the control plane node
2. Retrieve the node token from the control plane
3. Install K3s agent on worker nodes and join them to the cluster
4. Verify the cluster is running

### Reset/Remove K3s Cluster

To completely remove K3s from all nodes:

```bash
ansible-playbook k3s-reset.yml
```

This will uninstall K3s from all nodes and clean up directories.

### Access the Cluster

After successful installation, you can access the cluster from the control plane:

```bash
ssh ubuntu@192.168.178.81
kubectl get nodes
kubectl get pods -A
```

Or copy the kubeconfig to your local machine:

```bash
scp ubuntu@192.168.178.81:/etc/rancher/k3s/k3s.yaml ~/.kube/k3s-config
# Edit the file and change server: https://127.0.0.1:6443 to server: https://192.168.178.81:6443
export KUBECONFIG=~/.kube/k3s-config
kubectl get nodes
```

## Playbook Details

### k3s-setup.yml

- **Control Plane Setup:**
  - Installs K3s server with Traefik ingress controller enabled
  - Sets kubeconfig permissions to `644` for easy access
  - Retrieves the node token for workers to join

- **Worker Setup:**
  - Installs K3s agent
  - Automatically joins the control plane using the token
  - Verifies the agent is running

- **Verification:**
  - Waits for all nodes to be ready
  - Displays cluster status and running pods

### k3s-reset.yml

- Uninstalls K3s from all nodes
- Removes configuration directories
- Cleans up iptables rules on the control plane

### argocd-setup.yml

Installs and configures ArgoCD for GitOps-based deployments using existing manifests from `../manifests/apps/argo-cd/`.

**To install ArgoCD:**

```bash
cd ansible
ansible-playbook argocd-setup.yml
```

This playbook will:
1. Apply the ArgoCD namespace from `../manifests/apps/argo-cd/namespace.yaml`
2. Install ArgoCD using the official manifests
3. Wait for ArgoCD server to be ready
4. Apply the ArgoCD ingress from `../manifests/apps/argo-cd/ingress.yaml`
5. Retrieve and display the initial admin password

**Access ArgoCD UI:**

After installation:

1. Add to your `/etc/hosts`:
   ```bash
   echo "192.168.178.81 argocd.homelab.local" | sudo tee -a /etc/hosts
   ```

2. Access the UI at: `http://argocd.homelab.local`

3. Login with:
   - Username: `admin`
   - Password: (displayed at the end of the playbook or retrieve with):
     ```bash
     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
     ```

**Alternative: Port-forward (temporary access):**

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then access at: `https://localhost:8080`

## Troubleshooting

### Connection Issues

Test connectivity:
```bash
ansible all -m ping
```

### SSH Key Issues

Ensure your SSH key is added:
```bash
ssh-add ~/.ssh/id_rsa
```

### Check K3s Status

On control plane:
```bash
ssh ubuntu@192.168.178.81
sudo systemctl status k3s
```

On worker:
```bash
ssh ubuntu@192.168.178.82
sudo systemctl status k3s-agent
```

### View Logs

Control plane:
```bash
sudo journalctl -u k3s -f
```

Worker:
```bash
sudo journalctl -u k3s-agent -f
```

## Customization

### Traefik Ingress Controller

The playbook enables Traefik by default, providing an ingress controller out of the box. To disable it, add `--disable=traefik` to the install command in `k3s-setup.yml`:

```yaml
curl -sfL https://get.k3s.io | sh -s - server \
  --write-kubeconfig-mode=644 \
  --disable=traefik
```

### Additional K3s Options

You can add more K3s server options by modifying the install command:

```yaml
curl -sfL https://get.k3s.io | sh -s - server \
  --write-kubeconfig-mode=644 \
  --flannel-backend=vxlan \
  --cluster-cidr=10.42.0.0/16
```

See [K3s documentation](https://docs.k3s.io/installation/configuration) for all options.

## Next Steps

After the cluster is set up:
1. **Install ArgoCD** for GitOps deployments:
   ```bash
   ansible-playbook argocd-setup.yml
   ```
   (The playbook automatically applies namespace and ingress from `../manifests/apps/argo-cd/`)
2. **Access Traefik dashboard** at `http://traefik.homelab.local/dashboard/` (add to `/etc/hosts` first)
3. **Deploy your applications** using kubectl or ArgoCD from the `../manifests` directory
4. Configure additional Ingress resources to expose your applications
5. Add persistent storage if needed for stateful applications
