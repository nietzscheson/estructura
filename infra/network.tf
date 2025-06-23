data "aws_availability_zones" "this" {
  state = "available"
}

data "aws_subnets" "this" {
  filter {
    name   = "vpc-id"
    values = [aws_vpc.this.id]
  }
}

locals {
  availability_zone  = data.aws_availability_zones.this.names[0]
  availability_zones = slice(data.aws_availability_zones.this.names, 0, 2)
}

resource "aws_vpc" "this" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${local.name}"
  }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags = {
    Name = "${local.name}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }
  tags = {
    Name = "${local.name}-public"
  }
}

resource "aws_subnet" "public" {
  count                   = length(local.availability_zones)
  vpc_id                  = aws_vpc.this.id
  cidr_block              = cidrsubnet(aws_vpc.this.cidr_block, 8, count.index + 1)
  map_public_ip_on_launch = true
  availability_zone       = local.availability_zones[count.index]

  tags = {
    Name = "${local.name}-public-${count.index}"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(local.availability_zones)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}