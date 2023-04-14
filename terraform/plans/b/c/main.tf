terraform {
  required_version = "~> 1.3.2"
  required_providers {
    null = { version = "~> 3.2" }
  }
}

variable "dep" {
  type = string
}

resource "null_resource" "b" {
  triggers = {
    name = "b"
    dep  = var.dep
  }
}

resource "null_resource" "b-2" {
  count = 3
  triggers = {
    name  = "b-2"
    index = count.index
    dep   = var.dep
  }
}
