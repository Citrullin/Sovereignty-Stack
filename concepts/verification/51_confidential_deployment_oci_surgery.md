> *Part XIII: Decentralized Verification & The AI Auditor* — [← Back to Concepts Index](../README.md)

## 51. Confidential Deployment & OCI Surgery

The Sovereignty Stack rejects "Trust the Operator" and standard cloud container orchestration (e.g., Docker daemons, vulnerable CI/CD pipelines). Instead, it adopts **Root-of-Trust Maximalism**, extending zero-trust from the cloud down to constrained embedded devices through Trusted Execution Environments (TEEs) and OCI-native tooling.

### 51.1 Composite Container Images (The Ghost Layer)

Instead of building static, monolithic images using traditional Dockerfiles, or injecting configurations at runtime via insecure Helm templates, the stack utilizes **Dynamic Composition**.

1. **The Base Blob:** A cryptographically signed, read-only OCI image containing the core microservice or firmware.
2. **The Patch Layer:** Dedicated OCI layers containing jurisdiction- or device-specific configurations (e.g., `/etc/app/config` or localized assets).
3. **OCI Surgery:** Tools like `umoci` and `skopeo` are used to perform daemonless "surgery." They manipulate OCI manifests directly without pulling heavy blobs. This creates a "Ghost Layer"—a virtual image that is simply a JSON manifest pointing to the shared Base Blob and the specific Patch Blob.

Every layer is hashed and signed independently. If a base binary requires a security patch, the core is updated once; all dependent devices and configurations automatically inherit the fix via hash referencing, ensuring supply chain integrity with zero storage duplication.

### 51.2 The Three-Tier Sovereign Architecture

#### Tier 1: The Hardened Build Factory (Synthesis)
Standard CI/CD runners are entirely eliminated. Builds occur inside a **Trusted Execution Environment (TEE)** (Intel TDX / AMD SEV-SNP or Enarx/Veraison WebAssembly enclaves).
- **The Black Box:** Inside the hardware-encrypted TEE, `buildah` and `umoci` merge the Base and Patch layers. Because memory is encrypted, not even a malicious root sysadmin can inject a backdoor during the merge.
- **`in-toto` Attestations & Physical Protocols:** For embedded and constrained devices, compiling the firmware is not enough. The build factory generates an `in-toto` attestation linking the software to the **Physical Protocol**. Before a device is flashed, the attestation bundle includes:
  - The cryptographic signature of the OCI firmware image.
  - The hash of the X-ray scan of the physical USB cable used to flash the device.
  - The digital signatures (protocols) of the physical operators performing the flashing and X-raying.

#### Tier 2: The Attestation & Metadata Tier (The Tree)
- **Zot Registry:** A cloud-native OCI registry used to store the "Tree" of patches and Attestation Bundles, not just container images.
- **Keylime (Remote Boot Attestation):** The ultimate physical defense for hardware nodes. Keylime monitors the TPM (Trusted Platform Module) and PCR state. If a physical adversary swaps a "clean" component for a malicious one, the hardware state mismatch triggers a poison pill, wiping sovereign keys instantly.
- **Sigstore (Rekor):** An immutable transparency log recording every applied patch and hardware attestation.

#### Tier 3: The Runtime Tier (Confidential Deployment)
Once a clean image is deployed, it must be protected from the host OS (Sovereignty from the Provider).
- **Confidential Containers (CoCo):** Integrates Kata Containers with hardware enclaves. When Podman or Kubernetes starts the container, it runs inside a hardware-encrypted VM.
- **Key Broker Service (KBS):** The OCI image remains encrypted at rest in the registry. It is only decrypted inside the TEE *after* the TEE provides a hardware-signed quote proving it is running the exact "Hardened Image" specified in Tier 1.
- **`systemd-sysext`:** For host-level OS patching on Sovereign nodes, signed `.raw` images are dropped into `/var/lib/extensions`. The OS merges them immutably via OverlayFS—bringing OCI container-patching logic to the entire host operating system.
