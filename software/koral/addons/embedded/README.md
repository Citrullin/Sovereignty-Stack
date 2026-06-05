# Koral Embedded Addon: Constrained Device & Build Pipelines

This addon provides the build and mapping pipeline to generate **Koral Images** and **Koral Patches** for constrained edge devices, IoT modules, and embedded Point-of-Sale (POS) terminals.

## Build System Flexibility

This plugin supports compiling firmware configurations for various embedded operating systems (Yocto, Buildroot, Zephyr, FreeRTOS). It dynamically detects the build system configuration from `koral-project.yaml`.

To configure, define the following in the entity's `koral-project.yaml`:

```yaml
addons:
  embedded:
    enabled: true
    buildSystem: "yocto" # Supports "yocto", "buildroot", etc.
    targetDid: "did:koral:mapper:nxp-imx8-pos"
```
