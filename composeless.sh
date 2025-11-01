#!/bin/bash


function run() {
  local prefix=$1
  local port=$2
  local inner_port=$3
  local count=$4

  for i in $(seq 1 $count); do 
    local host_port=$((port + i))
    docker run -d --name "$prefix-$i" -p $host_port:$inner_port $prefix:latest
  done

}


function start() {
  for i in $(seq 1 $2); do 
    docker start "$1-$i"
  done
}


function stop() {
  for i in $(seq 1 $2); do 
    docker stop $1-$i
  done
}

function remove() {
  for i in $(seq 1 $2); do 
    docker rm $1-$i
  done
}


function usage() {
  echo "Usage: $0 run nginx 8000 80 10"
  echo "       $0 start nginx 10"
  echo "       $0 stop nginx 10"
  echo "       $0 rm nginx 10"
  exit 1
}


while [[ "$#" -gt 0 ]]; do
    case $1 in
      run)
	      shift 1
        run $@
        exit 1
	    ;;
      start)
	      shift 1
        start $@
        exit 1
	    ;;
      stop)
        shift 1
        stop $@
        exit 1
      ;;
      rm)
        shift 1
        remove $@
        exit 1
      ;;
      *)
        usage
      ;;
    esac
done
