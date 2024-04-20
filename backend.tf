terraform {
  backend "s3" {
    bucket         = "rajendra-terraform"
    key            = "wordpress.tfstate"
    region         = "ap-south-1"
  }
}