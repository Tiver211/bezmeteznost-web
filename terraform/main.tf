terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  zone                     = var.zone
  service_account_key_file = "key.json"
  folder_id                = "b1gvjr5sc8203q077glr"
  cloud_id                 = "b1g20pfn369hq0i21ihn"
}


# Общая сеть для всех ресурсов
resource "yandex_vpc_network" "main_network" {
  name = "main-bezmetejnost-network"
}

resource "yandex_vpc_subnet" "main-subnet" {
  name           = "main-subnet"
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.main_network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

# ВМ для Flask + Nginx
resource "yandex_compute_instance" "web" {
  name        = "flask-web"
  platform_id = "standard-v2"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd800c7s2p483i648ifv" # Ubuntu 20.04
      size     = 15
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.main-subnet.id
    nat       = true # Публичный IP
  }

  metadata = {
    ssh-keys = "tiver211:${var.ssh_public_key}"
  }
}

# ВМ для Minecraft
resource "yandex_compute_instance" "minecraft" {
  name        = "minecraft-server"
  platform_id = "standard-v2"

  resources {
    cores  = 6
    memory = 24
  }

  boot_disk {
    initialize_params {
      image_id = "fd800c7s2p483i648ifv" # Ubuntu 20.04
      size     = 50                     # Для мира Minecraft
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.main-subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "tiver211:${var.ssh_public_key}"
  }

  scheduling_policy {
    preemptible = true
  }
}

# DNS-зона (если домен делегирован в Yandex Cloud)
resource "yandex_dns_zone" "server" {
  name        = var.dns_zone_name_server
  description = "DNS for bezmetejnost.online"
  zone        = "bezmetejnost.online."
  public      = true
}

resource "yandex_dns_zone" "web" {
  name        = var.dns_zone_name
  description = "DNS for bezmetejnost.ru"
  zone        = "bezmetejnost.ru."
  public      = true
}

# Записи DNS
resource "yandex_dns_recordset" "web" {
  zone_id = yandex_dns_zone.web.id
  name    = "bezmetejnost.ru."
  type    = "A"
  ttl     = 600
  data    = [yandex_compute_instance.web.network_interface.0.nat_ip_address]
}

resource "yandex_dns_recordset" "minecraft" {
  zone_id = yandex_dns_zone.server.id
  name    = "bezmetejnost.online."
  type    = "A"
  ttl     = 600
  data    = [yandex_compute_instance.minecraft.network_interface.0.nat_ip_address]
}

# SmartCaptcha (через API Yandex Cloud)
resource "yandex_smartcaptcha_captcha" "demo-advanced-smartcaptcha" {
  name           = "bezmetejnost-web"
  complexity     = "EASY"
  pre_check_type = "SLIDER"
  challenge_type = "KALEIDOSCOPE"

}