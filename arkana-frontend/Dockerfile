FROM rust:1.75-slim as builder

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install trunk
RUN wget -qO- https://github.com/trunk-rs/trunk/releases/download/v0.18.8/trunk-x86_64-unknown-linux-gnu.tar.gz | tar -xzf- && \
    mv trunk /usr/local/bin/

# Install wasm target
RUN rustup target add wasm32-unknown-unknown

# Copy workspace
COPY Cargo.toml Cargo.lock ./
COPY arkana-frontend ./arkana-frontend
COPY arkana-shared ./arkana-shared

# Build WASM
WORKDIR /app/arkana-frontend
RUN trunk build --release

# Runtime - Nginx
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/arkana-frontend/dist /usr/share/nginx/html

# Nginx config
RUN echo 'server { \
    listen 80; \
    location / { \
    root /usr/share/nginx/html; \
    try_files $uri $uri/ /index.html; \
    } \
    location /api { \
    proxy_pass http://arkana-api:8000; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
