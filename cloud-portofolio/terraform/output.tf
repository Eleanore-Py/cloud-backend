output "instance_ip" {
  value = aws_instance.backend_server.public_ip
}