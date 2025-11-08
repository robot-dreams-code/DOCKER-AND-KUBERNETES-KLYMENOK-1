FROM golang:1.25.0-alpine3.22 AS build

RUN addgroup -S deploy && adduser -S deploy -G deploy

WORKDIR /app

# Best practice https://docs.docker.com/build/building/best-practices/#add-or-copy
RUN --mount=type=bind,source=go.mod,target=go.mod,readonly --mount=type=bind,source=go.sum,target=go.sum,readonly go mod download

# Give complete file ownership for deploy
COPY --chown=deploy:deploy --chmod=700 . .

RUN go build -o binary

FROM scratch AS target

# https://medium.com/@lizrice/non-privileged-containers-based-on-the-scratch-image-a80105d6d341
COPY --from=build /etc/group /etc/group
COPY --from=build /etc/passwd /etc/passwd

# Granting read and execute permissions
COPY --from=build --chown=deploy:deploy --chmod=500 /app/binary /app/binary

EXPOSE 8080

USER deploy:deploy

ENTRYPOINT [ "/app/binary" ]