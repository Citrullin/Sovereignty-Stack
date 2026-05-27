FROM clux/muslrust:stable AS chef
WORKDIR /siwe-oidc
RUN cargo install cargo-chef

FROM chef as dep_planner
COPY ./src/ ./src/
COPY ./Cargo.lock ./
COPY ./Cargo.toml ./
COPY ./siwe-oidc.toml ./
RUN cargo chef prepare  --recipe-path recipe.json

FROM chef as dep_cacher
COPY --from=dep_planner /siwe-oidc/recipe.json recipe.json
ENV RUST_MIN_STACK=33554432
RUN cargo chef cook --release --jobs 1 --recipe-path recipe.json

FROM node:16-alpine as node_builder
ARG PROJECT_ID
ENV PROJECT_ID=${PROJECT_ID}
ADD --chown=node:node ./static /siwe-oidc/static
ADD --chown=node:node ./js/ui /siwe-oidc/js/ui
WORKDIR /siwe-oidc/js/ui
RUN npm install
RUN npm run build

FROM chef as builder
COPY --from=dep_cacher /siwe-oidc/target/ ./target/
COPY --from=dep_cacher $CARGO_HOME $CARGO_HOME
COPY --from=dep_planner /siwe-oidc/ ./
ENV RUST_MIN_STACK=33554432
RUN cargo build --release --jobs 1

FROM alpine
COPY --from=builder /siwe-oidc/target/x86_64-unknown-linux-musl/release/siwe-oidc /usr/local/bin/
WORKDIR /siwe-oidc
RUN mkdir -p ./static
COPY --from=node_builder /siwe-oidc/static/ ./static/
COPY --from=builder /siwe-oidc/siwe-oidc.toml ./
ENV SIWEOIDC_ADDRESS="0.0.0.0"
EXPOSE 8000
ENTRYPOINT ["siwe-oidc"]
LABEL org.opencontainers.image.source https://github.com/signinwithethereum/siwe-oidc
LABEL org.opencontainers.image.description "OpenID Connect Identity Provider for Sign-In with Ethereum"
LABEL org.opencontainers.image.licenses "MIT OR Apache-2.0"
