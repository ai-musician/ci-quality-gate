variable "env_prefix" {
  description = "Prefix for the generated test environment name."
  type        = string
  default     = "ci-test"
}

variable "region" {
  description = "Cloud region the test environment models (placeholder)."
  type        = string
  default     = "us-west-2"
}

variable "api_port" {
  description = "Port the test API service listens on."
  type        = number
  default     = 8000
}
