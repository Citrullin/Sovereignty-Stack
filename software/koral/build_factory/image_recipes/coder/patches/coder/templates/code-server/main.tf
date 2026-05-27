terraform {
  required_providers {
    coder = {
      source  = "coder/coder"
      version = "~> 0.23.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.18"
    }
  }
}

provider "coder" {}

variable "istio_ingress_ip" {
  type        = string
  description = "The ClusterIP of the istio-ingress service"
}

variable "homelab_domain" {
  type        = string
  description = "The homelab domain (e.g., homelab.local)"
}



data "coder_parameter" "language" {
  name         = "Language"
  display_name = "Programming Language"
  description  = "Select the programming language environment"
  default      = "javascript"
  mutable      = true 
  
  option {
    name  = "JavaScript (Node.js)"
    value = "javascript"
  }
  option {
    name  = "Golang"
    value = "golang"
  }
  option {
    name  = "Scala"
    value = "scala"
  }
}

data "coder_workspace" "me" {}

resource "coder_agent" "main" {
  os   = "linux"
  arch = "amd64"
  dir  = "/home/coder"

  # Install tools based on selected language
  startup_script = <<EOT
    #!/bin/bash
    set -e

    # Start code-server
    code-server --auth none --port 13337 >/tmp/code-server.log 2>&1 &

    # Language Setup
    LANGUAGE="${data.coder_parameter.language.value}"
    
    echo "Setting up environment for $LANGUAGE..."
    
    if [ "$LANGUAGE" == "javascript" ]; then
        if ! command -v node &> /dev/null; then
            curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
            sudo apt-get install -y nodejs
        fi
    elif [ "$LANGUAGE" == "golang" ]; then
        if ! command -v go &> /dev/null; then
            wget -q https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
            sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
            echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
            rm go1.21.6.linux-amd64.tar.gz
        fi
    elif [ "$LANGUAGE" == "scala" ]; then
        if ! command -v cs &> /dev/null; then
            curl -fL https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz | gzip -d > cs && chmod +x cs && ./cs setup -y
            echo 'export PATH=$PATH:/home/coder/.local/share/coursier/bin' >> ~/.bashrc
        fi
    fi
  EOT
}

resource "coder_app" "code-server" {
  agent_id     = coder_agent.main.id
  slug         = "code-server"
  display_name = "VS Code Web"
  url          = "http://localhost:13337/?folder=/home/coder"
  subdomain    = false
  share        = "owner"

  healthcheck {
    url       = "http://localhost:13337/healthz"
    interval  = 5
    threshold = 6
  }
}

resource "kubernetes_persistent_volume_claim" "home" {
  metadata {
    name = "coder-${data.coder_workspace.me.owner}-${data.coder_workspace.me.name}-home"
    namespace = "coder"
    labels = {
      "app.kubernetes.io/name"     = "coder-workspace"
      "app.kubernetes.io/instance" = "coder-workspace-${data.coder_workspace.me.owner}-${data.coder_workspace.me.name}"
      "app.kubernetes.io/part-of"  = "coder"
    }
  }
  wait_until_bound = false
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "10Gi"
      }
    }
  }
}

resource "kubernetes_pod" "main" {
  count = data.coder_workspace.me.start_count
  metadata {
    name = "coder-${data.coder_workspace.me.owner}-${data.coder_workspace.me.name}"
    namespace = "coder"
    labels = {
        "app.kubernetes.io/name"     = "coder-workspace"
    }
  }
  spec {
    # Use Istio Ingress IP for internal resolution of homelab domains
    host_aliases {
      ip = var.istio_ingress_ip
      hostnames = [
        "authentik.${var.homelab_domain}",
        "coder.${var.homelab_domain}"
      ]
    }
    security_context {
      run_as_user = 1000
      fs_group    = 1000
    }
    
    container {
      name    = "dev"
      image   = "codercom/code-server:latest"
      command = ["sh", "-c", coder_agent.main.init_script]
      security_context {
        run_as_user = 1000
      }
      env {
        name  = "CODER_AGENT_TOKEN"
        value = coder_agent.main.token
      }
      # CA Trust for Agent Connectivity
      env {
        name  = "CODER_AGENT_CA_FILE"
        value = "/etc/ssl/certs/homelab-ca.crt"
      }
      env {
        name  = "CURL_CA_BUNDLE"
        value = "/etc/ssl/certs/homelab-ca.crt"
      }
      volume_mount {
        mount_path = "/home/coder"
        name       = "home"
        read_only  = false
      }
      volume_mount {
        name       = "homelab-ca"
        mount_path = "/etc/ssl/certs/homelab-ca.crt"
        sub_path   = "homelab-ca.crt"
        read_only  = true
      }
    }

    volume {
      name = "home"
      persistent_volume_claim {
        claim_name = kubernetes_persistent_volume_claim.home.metadata.0.name
      }
    }
    volume {
      name = "homelab-ca"
      config_map {
        name = "homelab-ca"
      }
    }
  }
}
