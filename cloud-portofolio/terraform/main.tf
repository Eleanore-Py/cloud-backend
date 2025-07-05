provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "backend_server" {
  ami           = "ami-0fc5d935ebf8bc3bc"  # Ubuntu 22.04 (Singapore)
  instance_type = var.instance_type
  key_name      = var.key_name

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install docker.io -y
              docker run -d -p 5000:5000 dhava/backend-app:latest
              EOF

  tags = {
    Name = "CloudFlaskApp"
  }

  associate_public_ip_address = true

  vpc_security_group_ids = [aws_security_group.allow_http.id]
}

resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow 5000 from internet"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}