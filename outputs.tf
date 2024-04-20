output "instance_ip" {
  value = aws_instance.wordpress.public_ip
  description = "The public IP address of the EC2 instance."
}