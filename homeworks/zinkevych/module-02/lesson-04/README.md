# Building image from project root
`docker build -f homeworks/zinkevych/module-02/lesson-04/Dockerfile -t py-lesson-4 .`

# Run Dockerfile container on port 8080 with env values
`docker run -p 8080:8080 --env-file homeworks/zinkevych/module-02/lesson-04/.env py-lesson-4`

# Run docker-compose.yaml from workspace root
- `cd homeworks/zinkevych/module-02/lesson-04/`
- `docker compose up`