FROM  harbor.avalaunch.aval/docker-hub-proxy/golang:1.23 AS build
WORKDIR /apps/simple-app 

COPY go.mod go.sum ./

#bad things here to fix certificate problems
#0.375 go: github.com/gorilla/mux@v1.8.1: Get "https://proxy.golang.org/github.com/gorilla/mux/@v/v1.8.1.mod": tls: failed to verify certificate: x509: certificate signed by unknown authority
# and 0.541 go: github.com/gorilla/mux@v1.8.1: reading github.com/gorilla/mux/go.mod at revision v1.8.1: git ls-remote -q origin in /go/pkg/mod/cache/vcs/ebce69d65fcbb10d46c06b9a96d0b75cbef4f6fe72077ff7900bc6194bb0d703: exit status 128:
#0.541 	fatal: unable to access 'https://github.com/gorilla/mux/': server certificate verification failed. CAfile: none CRLfile: none
ENV GOPROXY=direct
RUN git config --global http.sslVerify false

RUN go mod download
COPY  . .

RUN go build -o /bin/app ./main.go


FROM harbor.avalaunch.aval/docker-hub-proxy/debian:stable-20251103-slim
WORKDIR /apps/simple-app

RUN useradd runapp
USER runapp

COPY --from=build /bin/app /apps/simple-app/bin/app

EXPOSE 8080
CMD ["/apps/simple-app/bin/app"]
