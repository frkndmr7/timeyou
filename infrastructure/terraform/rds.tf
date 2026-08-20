resource "aws_security_group" "rds" {
  name        = "${var.cluster_name}-rds"
  description = "Allow PostgreSQL access from the EKS cluster security group."
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.cluster_name}-rds"
  }
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_eks" {
  security_group_id            = aws_security_group.rds.id
  referenced_security_group_id = aws_eks_cluster.main.vpc_config[0].cluster_security_group_id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  description                  = "PostgreSQL from EKS managed node ENIs."
}

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.cluster_name}-postgres"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.cluster_name}-postgres"
  }
}

resource "aws_db_instance" "postgres" {
  identifier                  = "${var.cluster_name}-postgres"
  engine                      = "postgres"
  instance_class              = "db.t4g.micro"
  allocated_storage           = 20
  storage_type                = "gp3"
  storage_encrypted           = true
  publicly_accessible         = false
  multi_az                    = false
  db_name                     = var.database_name
  username                    = var.database_username
  manage_master_user_password = true
  port                        = 5432
  db_subnet_group_name        = aws_db_subnet_group.postgres.name
  vpc_security_group_ids      = [aws_security_group.rds.id]
  backup_retention_period     = 1
  apply_immediately           = true
  deletion_protection         = false
  skip_final_snapshot         = true

  tags = {
    Name = "${var.cluster_name}-postgres"
  }
}
