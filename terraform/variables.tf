variable "zone" {
  type    = string
  default = "ru-central1-b"
}

variable "network" {
  type    = string
  default = "ya-network"
}

variable "subnet" {
  type    = string
  default = "ya-network"
}

variable "nat" {
  type    = bool
  default = true
}

variable "ssh_public_key" {
  type = string
}

variable "cores" {
  type    = number
  default = 2
}

variable "memory" {
  type    = number
  default = 4
}

variable "dns_zone_name" {
  type    = string
  default = "bezmetejnost-ru"
}

variable "dns_zone_name_server" {
  type    = string
  default = "bezmetejnost-online"
}