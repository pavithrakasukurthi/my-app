resource "aws_instance" "docker" {
    ami = local.ami_id
    instance_type = "t3.micro"
    vpc_security_group_ids = [aws_security_group.docker.id]
    tags = {
        Name = "${var.project}-${var.environment}-docker"
    }
     root_block_device {
        volume_size = 50
        volume_type = "gp3" # or "gp2", depending on your preference
    }

    user_data = file("extend.sh")
}

resource "aws_security_group" "docker" {
    name = "roboshop-docker"
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8000
        to_port = 8000
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_route53_record" "docker" {
    name = "docker.${var.domain_name}"
    zone_id = var.zone_id
    type = "A"
    ttl = 1
    records = [aws_instance.docker.public_ip]
    allow_overwrite = true
}