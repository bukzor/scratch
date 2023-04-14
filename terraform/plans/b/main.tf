terraform {
  required_version = "~> 1.3.2"
  required_providers {
    null = { version = "~> 3.2" }
    time = { version = "~> 0.9" }
  }
}

# variable "dep" {
#   type = string
# }

resource "time_static" "time-1" {}

resource "null_resource" "b-1" {
  triggers = {
    name = "b-1"
    time = time_static.time-1.rfc3339
  }
}

resource "time_static" "time-2" {
  triggers = {
    b-1 = jsonencode(null_resource.b-1)
  }
}

resource "null_resource" "b-2" {
  triggers = {
    name = "b-2"
    time = time_static.time-2.rfc3339
  }
}
