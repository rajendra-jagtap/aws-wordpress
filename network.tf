module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = var.vpc_name
  cidr = var.vpc_cidr
  azs  = var.azs

  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway = true
  single_nat_gateway = true

  public_subnet_tags = {
    "Name" = "Public"
    "Type" = "Public"
  }

  private_subnet_tags = {
    "Name" = "Private"
    "Type" = "Private"
  }

  tags = {
    "Environment" = "Dev"
  }
}