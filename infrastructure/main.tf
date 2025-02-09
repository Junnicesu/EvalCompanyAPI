terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "evalcompimg" {
  name         = "tobexinminsu/evalcompanyapi:0.0.1"  # Replace with your image name
  keep_locally = false  # Ensures the image stays on your system
}

resource "docker_container" "evalcomp_container" {
  name  = "evalcompapi"
  image = docker_image.evalcompimg.name

  ports {
    internal = 8000
    external = 8000
  }

  restart = "always"
}
