FROM  golang:1.23 AS build
WORKDIR /apps/simple-app 

COPY go.mod go.sum ./

#bad things here to fix certificate problems
ENV GOPROXY=direct
RUN git config --global http.sslVerify false

RUN go mod download
COPY  . .

RUN go build -o /bin/app ./main.go


FROM debian:stable-20251103-slim
WORKDIR /apps/simple-app

RUN useradd runapp
USER runapp

COPY --from=build /bin/app /apps/simple-app/bin/app

EXPOSE 8080
CMD ["/apps/simple-app/bin/app"]