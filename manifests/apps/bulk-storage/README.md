# bulk-storage

A second [local-path-provisioner](https://github.com/rancher/local-path-provisioner)
instance that provides the `bulk` StorageClass. Volumes land on each node's
secondary drive, mounted at `/mnt/bulk`:

| Node         | Drive                      | Mount     |
|--------------|----------------------------|-----------|
| controlplane | 256 GB SK hynix SSD        | /mnt/bulk |
| worker-1     | 1 TB WD Green HDD (5400rpm)| /mnt/bulk |

Use it like the default `local-path` class, just set `storageClassName: bulk`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: media
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: bulk
  resources:
    requests:
      storage: 100Gi
```

Notes:

- `volumeBindingMode: WaitForFirstConsumer`: the directory is created on the
  node where the first pod is scheduled, and the volume is pinned to that node.
- Add a `nodeSelector` on the pod if the choice of drive matters (the HDD on
  worker-1 is large and slow, the SSD on controlplane is small and fast).
- `reclaimPolicy: Delete`: deleting the PVC removes the directory on the drive.
- Only nodes listed in `configmap.yaml` can host `bulk` volumes.
