# Configure the Kubernetes provider
provider "kubernetes" {
  config_path = "~/.kube/config"  # Assumes kubeconfig is set up in the playground
}

# Define a variable for BASE_XML_URL
variable "BASE_XML_URL" {
  type = string
  description = "URL of the XML API endpoint"
}

# Define the Kubernetes Deployment
resource "kubernetes_deployment" "evalcompanyapi" {
  metadata {
    name = "evalcompanyapi"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "evalcompanyapi"
      }
    }
    template {
      metadata {
        labels = {
          app = "evalcompanyapi"
        }
      }
      spec {
        containers {
          image = "tobexinminsu/evalcompanyapi:0.0.2"
          name  = "evalcompanyapi"
          ports {
            container_port = 8000  # FastAPI typically runs on port 8000
          }
          env {
            name  = "BASE_XML_URL"
            value = var.BASE_XML_URL  # Pass the XML API URL to the container
          }
        }
      }
    }
  }
}

# Define the Kubernetes Service
resource "kubernetes_service" "evalcompanyapi" {
  metadata {
    name = "evalcompanyapi-service"
  }
  spec {
    selector = {
      app = "evalcompanyapi"
    }
    ports {
      port        = 80
      target_port = 8000
      node_port   = 30000  # Optional: specify a port between 30000-32767
    }
    type = "NodePort"  # Use NodePort for external access in the playground
  }
}