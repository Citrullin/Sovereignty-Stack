# Verification & Auditing: Confidential Deployment & OCI Surgery

> *Part XIII: Decentralized Verification & The AI Auditor* — [← Back to Architecture Index](../README.md)

## 51. Confidential Deployment & OCI Surgery: Hardware-Enforced Sovereignty

In conventional cloud environments, the host infrastructure provider or cloud administrator retains ultimate control over execution memory and container storage, presenting a critical security risk under the **Regulated Banking Well**. 

The Sovereign Manifold framework rejects "trust the operator" models. Instead, it adopts **Root-of-Trust Maximalism**, extending hardware-secured, zero-trust cryptographic guarantees from local edge-running microservices down to constrained embedded devices and Point-of-Sale (POS) terminals through Trusted Execution Environments (TEEs) and OCI-native tooling.

---

### 51.1. Composite Container Images & OCI Surgery

Rather than building heavy, monolithic container images via traditional Dockerfiles or injecting configurations at runtime via insecure environment variables, the platform leverages **Dynamic OCI Composition**:

1. **The Base Cryptographic Blob:** A read-only, signed OCI container image containing the core application logic, system binaries, or device firmware.
2. **The Localized Patch Layer:** Dedicated, lightweight OCI layers containing specific regional configurations, cryptographic identities, or device parameters.
3. **Daemonless OCI Surgery:** Using specialized utility tools (such as `umoci` and `skopeo`), the deployment client executes "OCI Surgery." It manipulates container manifests directly without requiring a running Docker daemon or pulling massive base blobs. This generates a "Ghost Layer"—a virtual image representation that is simply a JSON manifest pointing directly to the shared, read-only Base Blob and the specific, encrypted Patch Layer.

Every layer is hashed and signed independently. If a vulnerability is patched in the base image, the base blob is updated once. All downstream edge nodes and active terminals automatically inherit the security updates via cryptographic hash referencing, ensuring absolute supply chain integrity with zero storage duplication.

---

### 51.2. The Three Architectural Tiers of System Synthesis

To guarantee that software cannot be tampered with between compilation and execution, the platform implements a three-tier deployment synthesis pipeline:

#### Tier 1: The Hardened Build Factory (Synthesis)
Traditional, vulnerable CI/CD runner machines are eliminated. Binary compilation and image creation occur inside a hardware-encrypted **Trusted Execution Environment (TEE)** (such as AMD SEV-SNP, Intel TDX, or Enarx WebAssembly enclaves).
- **The Black Box Merge:** Inside the TEE, `buildah` and `umoci` merge the Base and Patch layers. Because memory space is hardware-encrypted, not even a host system administrator with root access can inspect execution memory or inject backdoors.
- **Physical Protocol & `in-toto` Attestations:** For constrained edge devices and POS terminals, compiling the software is insufficient. The build factory generates an `in-toto` attestation linking the digital software release to the physical deployment protocol. Before a device is flashed, the attestation bundle digests:
  - The cryptographic signature of the compiled OCI firmware.
  - The hash of the X-ray scan of the physical data cable utilized to write the binary.
  - The digital signatures (NFC taps) of the physical operators executing the flashing and inspection process.

#### Tier 2: The Attestation & Metadata Registry (Storage & Boot Auditing)
- **Zot Registry:** An OCI-native registry used to host the entire tree of configuration patches, container layers, and signed attestation bundles.
- **Keylime (Remote Boot Attestation):** Provides remote platform integrity monitoring. Keylime continuously monitors the Trusted Platform Module (TPM) and Platform Configuration Register (PCR) states of active hardware nodes. If an adversary attempts to swap physical components or tamper with the bootloader, the resulting cryptographic state mismatch immediately triggers a "poison pill" routine, erasing local sovereign keys.
- **Sigstore (Rekor):** An immutable transparency log recording every applied configuration patch and hardware attestation.

#### Tier 3: The Confidential Runtime Tier (Execution)
Once deployed, the runtime environment isolates the application from host operating system vulnerabilities and hypervisor-level attacks:
- **Confidential Containers (CoCo):** Integrates Kata Containers with hardware enclaves. When Podman or Kubernetes initiates the container, it executes inside a hardware-encrypted virtual machine.
- **Key Broker Service (KBS):** The OCI image remains encrypted at rest within the registry. The decryption key is only released by the KBS inside the TEE after the enclave provides a hardware-signed cryptographic quote proving it is running the exact, untampered container image verified in Tier 1.
- **`systemd-sysext` OS Extensions:** Host-level operating system patching is managed by dropping signed `.raw` system images into `/var/lib/extensions`. The host OS merges them immutably at runtime via OverlayFS, applying container-patching paradigms to the underlying system.
