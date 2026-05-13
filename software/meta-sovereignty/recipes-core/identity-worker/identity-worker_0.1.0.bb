# TODO/FIXME: Rough implementation of the end-to-end sociological blockchain framework auditor.
# This recipe is currently a mock outline.
# Next steps:
# - Connect SRC_URI to actual Rust module path.
# - Configure target triple to match hardware specifications (e.g., bit.block/gachapon).
# - Integrate swTPM dependencies for local QEMU simulation.

SUMMARY = "Sovereign Stack Identity Worker"
DESCRIPTION = "The Rust-based Finite State Machine (FSM) executing VSSS math inside the TEE enclave."
HOMEPAGE = "https://github.com/citrullin/sovereign_stack_vision"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit cargo

SRC_URI = "file://identity-worker \
           "
# In a real environment, SRC_URI would point to the local git path or a tarball of the rust code.

# DEPENDS on threshold-crypto and required libraries
DEPENDS = "openssl"

# Specify the path to the Cargo.toml
CARGO_SRC_DIR = "identity-worker"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/target/${TARGET_SYS}/release/identity-worker ${D}${bindir}/
}
