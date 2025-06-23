resource "aws_db_subnet_group" "this" {
  name       = local.name
  subnet_ids = data.aws_subnets.this.ids
}

resource "aws_db_instance" "this" {
  depends_on                          = [random_password.database]
  identifier                          = local.name
  db_name                             = "postgres"
  username                            = "postgres"
  password                            = random_password.database.result
  port                                = "5432"
  engine                              = "postgres"
  engine_version                      = "17.4"
  instance_class                      = "db.t3.micro"
  allocated_storage                   = "20"
  storage_encrypted                   = false
  vpc_security_group_ids              = [aws_security_group.rds.id]
  db_subnet_group_name                = aws_db_subnet_group.this.name
  multi_az                            = false
  storage_type                        = "gp3"
  publicly_accessible                 = true
  backup_retention_period             = 7
  skip_final_snapshot                 = true
  apply_immediately                   = true
  iam_database_authentication_enabled = true
}