first stage in golang image to install dependencies and compile go.
second stage is scratch image only with binary in it what made image extremely small - downside is that we cannot connect into container and tinker with it since we lack coreutils.

