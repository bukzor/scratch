terraform {
  required_version = "~> 1.3.2"
  required_providers {
    null = { version = "~> 3.2" }
    time = { version = "~> 0.9" }
  }
}

module "b" {
  source = "./b"
  # dep    = null_resource.root-3["black"].triggers.index
  # depends_on = [null_resource.root-3]
}
