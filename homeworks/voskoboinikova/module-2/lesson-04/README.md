to build an image:
1) a valid crt.crt must be in a course-app dir
2) when running build command, specify actual build-arg values
docker build  --build-arg CORP_REGISTRY="somename" --build-arg CORP_HOST="repo.corp.local" --build-arg CORP_INDEX="index.corp.local"  --build-arg CORP_INDEX_URL="https://repo.corp.local/simple" -t course-app:v1.0   -f Dockerfile    ..\..\..\..\apps\course-app

before running compose up set env variable to the actual value
set  CORP_REGISTRY="somename"
