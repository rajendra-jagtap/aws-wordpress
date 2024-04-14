variable "aws_region" {
  description = "AWS region to deploy resources into"
  default     = "ap-southeast-1"
}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "azs" {
  description = "Availability Zones"
  type        = list(string)
}

variable "public_subnets" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
}

variable "private_subnets" {
  description = "CIDR blocks for the private subnets"
  type        = list(string)
}

variable "instance_type" {
  description = "Instance Type of Wordpress Instance"
  type        = string
}

variable "ami_id" {
  description = "Base AMI for Wordpress Instance"
  type        = string
}

variable "key_name" {
  description = "Keypair for Wordpress Instance"
  type        = string
}