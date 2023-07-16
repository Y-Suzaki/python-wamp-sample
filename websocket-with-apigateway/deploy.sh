#!/bin/bash -e

stack_name_app="apigateway-websocket-lambda"

echo "** Start to deploy and build. **"

S3_BUCKET="cf-templates-461spye58s2i-ap-northeast-1"
#echo "Upload open-api.yml on s3"
#aws s3 cp docs/open-api.yml s3://cf-templates-461spye58s2i-ap-northeast-1/

echo "Zip python codes"
mkdir -p lambda
cp infra/web-api.yml lambda/
cp -r app/ lambda/
cd lambda/app
#pip install -r requirements.txt -t .
zip -r ../lambda.zip ./*
cd ..

echo "Build serverless function..."
aws cloudformation package \
  --template-file web-api.yml \
  --output-template-file web-api-deploy.yml \
  --s3-bucket "${S3_BUCKET?}" \
  --s3-prefix apigateway-websocket \
  --region ap-northeast-1 \
  --profile default

echo "Deploy serverless function..."
aws cloudformation deploy \
  --template-file web-api-deploy.yml \
  --stack-name ${stack_name_app} \
  --capabilities CAPABILITY_NAMED_IAM \
  --region ap-northeast-1 \
  --profile default

echo "** All complete! **"
aws s3 rm s3://"${S3_BUCKET?}"/apigateway-websocket/ \
  --region ap-northeast-1 \
  --profile default \
  --recursive

cd ..
rm -rf lambda/
