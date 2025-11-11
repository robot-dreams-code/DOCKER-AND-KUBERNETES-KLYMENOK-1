FROM golang:1.20-alpine AS builder
WORKDIR /apps/third-app
COPY apps/simple-app/go.mod .
COPY apps/simple-app/go.sum .
RUN go mod download
COPY apps/simple-app/*.go .
RUN go build -o main ./

FROM scratch
COPY --from=builder /apps/third-app/main .
EXPOSE 8080
RUN useradd appuser
USER appuser
CMD [ "./main" ]




