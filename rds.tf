#module "rds" {
#  source  = "terraform-aws-modules/rds/aws"
#  version = "~> 4.0"
#
#  identifier        = "wordpress-db"
#  engine            = "mysql"
#  engine_version    = "8.0"
#  instance_class    = "db.t3.small"
#  allocated_storage = 20
#  db_name           = "wordpressdb"
#  username          = "wpuser"
#  password          = var.db_password
#  multi_az          = false
#  subnets           = var.db_subnets
#}