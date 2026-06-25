output "environment_name" {
  description = "Unique name of the provisioned test environment."
  value       = local.environment_name
}

output "manifest_path" {
  description = "Path to the generated test-environment manifest."
  value       = local_file.test_env_manifest.filename
}
