output "instance_ip" {
  value = aws_instance.web.public_ip
  description = "The public IP address of the EC2 instance."
}