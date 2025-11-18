FROM golang:1.23-alpine AS builder
WORKDIR /apps/third-app
COPY apps/simple-app/go.mod .
COPY apps/simple-app/go.sum .
COPY apps/simple-app/static ./static
COPY apps/simple-app/templates ./templates

RUN go mod download
COPY apps/simple-app/*.go .

RUN go build -o main ./

RUN apk add --no-cache shadow && useradd appuser

FROM scratch
COPY --from=builder /apps/third-app/main .
EXPOSE 8080

USER appuser
CMD [ "./main" ]




