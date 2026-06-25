terraform {
  required_version = ">= 1.5"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

# A unique suffix so every provisioned test environment is isolated and
# reproducible — no two `apply`s collide. This mirrors how ephemeral CI test
# environments are kept independent from one another.
resource "random_id" "env_suffix" {
  byte_length = 4
}

locals {
  environment_name = "${var.env_prefix}-${random_id.env_suffix.hex}"
}

# The "test environment manifest" this IaC produces. In a real setup these
# would be cloud resources (VPC, subnets, a test database). Here it's a local
# file so the demo runs free, offline, and without cloud credentials — while
# still exercising the full Terraform lifecycle: init / plan / apply / destroy.
resource "local_file" "test_env_manifest" {
  filename = "${path.module}/generated/${local.environment_name}.json"
  content = jsonencode({
    environment = local.environment_name
    region      = var.region
    services = {
      api_port = var.api_port
      db_name  = "testdb_${random_id.env_suffix.hex}"
    }
  })
}
