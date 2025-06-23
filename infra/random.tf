resource "random_password" "database" {
  length  = 40
  special = false
  upper   = true # Incluir letras mayúsculas
  lower   = true # Incluir letras minúsculas
  #min_special      = 1
  #override_special = "!#$%^*()-_=+[]{}<>?:"
  keepers = {
    pass_version = 1
  }
}