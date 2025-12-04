#I took golang:1.23 as with building 1.20  Igot errorr
FROM golang:1.23-alpine AS builder  
WORKDIR /apps/third-app
COPY apps/simple-app/go.mod .
COPY apps/simple-app/go.sum .
#add coping of static and templates folders as without these folders the application won't work  
COPY apps/simple-app/static ./static
COPY apps/simple-app/templates ./templates

RUN go mod download
COPY apps/simple-app/*.go .

RUN go build -o main ./
#apk add & useradd, alpine is a minimal image and doesn't have useradd by default  
RUN apk add --no-cache shadow && useradd appuser

FROM scratch
COPY --from=builder /apps/third-app/main .
#add copying of /etc/passwd to have appuser in final image
COPY --from=builder /etc/passwd /etc/passwd
EXPOSE 8080

USER appuser
CMD [ "./main" ]




