###
# Bucket For Files
##

resource "aws_s3_bucket" "files" {
  bucket = "${local.name}-files"
}

resource "aws_s3_bucket_public_access_block" "files" {
  bucket = aws_s3_bucket.files.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
resource "aws_s3_bucket_policy" "files" {
  bucket = aws_s3_bucket.files.id

  depends_on = [aws_s3_bucket_public_access_block.files]

  policy = jsonencode({
    Statement = [
      {
        "Sid" : "PublicListGet",
        "Effect" : "Allow",
        "Principal" : "*",
        "Action" : [
          "s3:List*",
          "s3:Get*"
        ],
        "Resource" : [
          "arn:aws:s3:::${aws_s3_bucket.files.id}",
          "arn:aws:s3:::${aws_s3_bucket.files.id}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket" "nix" {
  bucket = "${local.name}-nix"
}

###
# Bucket For My
##

#resource "aws_s3_bucket" "my" {
#  bucket = "${local.name}-my"
#}
#
#resource "aws_s3_bucket_public_access_block" "my" {
#  bucket = aws_s3_bucket.my.id
#
#  block_public_acls       = false
#  block_public_policy     = false
#  ignore_public_acls      = false
#  restrict_public_buckets = false
#}
#resource "aws_s3_bucket_policy" "my" {
#  bucket = aws_s3_bucket.my.id
#
#  depends_on = [aws_s3_bucket_public_access_block.my]
#
#  policy = jsonencode({
#    Statement = [
#      {
#        "Sid" : "PublicReadGetObject",
#        "Effect" : "Allow",
#        "Principal" : "*",
#        "Action" : "s3:GetObject",
#        "Resource" : "arn:aws:s3:::${aws_s3_bucket.my.id}/*"
#      },
#    ]
#  })
#}
#
#resource "aws_s3_bucket_website_configuration" "my" {
#  bucket = aws_s3_bucket.my.id
#
#  index_document {
#    suffix = "index.html"
#  }
#}
#
#resource "aws_s3_bucket_versioning" "my" {
#  bucket = aws_s3_bucket.my.id
#  versioning_configuration {
#    status = "Enabled"
#  }
#}

resource "aws_s3_bucket" "my" {
  bucket = "${local.name}-my"
}

resource "aws_s3_bucket_public_access_block" "my" {
  bucket = aws_s3_bucket.my.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
resource "aws_s3_bucket_policy" "my" {
  bucket = aws_s3_bucket.my.id

  depends_on = [aws_s3_bucket_public_access_block.my]

  policy = jsonencode({
    Statement = [
      {
        "Sid" : "PublicListGet",
        "Effect" : "Allow",
        "Principal" : "*",
        "Action" : [
          "s3:List*",
          "s3:Get*",
          "s3:Put*",
        ],
        "Resource" : [
          "arn:aws:s3:::${aws_s3_bucket.my.id}",
          "arn:aws:s3:::${aws_s3_bucket.my.id}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket_cors_configuration" "my" {
  bucket = aws_s3_bucket.my.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_website_configuration" "my" {
  bucket = aws_s3_bucket.my.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_versioning" "my" {
  bucket = aws_s3_bucket.my.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "samples" {
  bucket = "${local.name}-samples"
}

resource "null_resource" "upload_test_files" {
  provisioner "local-exec" {
    command = "aws s3 cp ../core/tests/files s3://${aws_s3_bucket.samples.bucket}/ --recursive"
  }

  depends_on = [aws_s3_bucket.samples]
}


###
# Bucket For WWW
##

resource "aws_s3_bucket" "www" {
  bucket = "${local.name}-www"
}

resource "aws_s3_bucket_public_access_block" "www" {
  bucket = aws_s3_bucket.www.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
resource "aws_s3_bucket_policy" "www" {
  bucket = aws_s3_bucket.www.id

  depends_on = [aws_s3_bucket_public_access_block.www]

  policy = jsonencode({
    Statement = [
      {
        "Sid" : "PublicReadGetObject",
        "Effect" : "Allow",
        "Principal" : "*",
        "Action" : "s3:GetObject",
        "Resource" : "arn:aws:s3:::${aws_s3_bucket.www.id}/*"
      },
    ]
  })
}

resource "aws_s3_bucket_website_configuration" "www" {
  bucket = aws_s3_bucket.www.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_versioning" "www" {
  bucket = aws_s3_bucket.www.id
  versioning_configuration {
    status = "Enabled"
  }
}