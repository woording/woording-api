#! /bin/sh

if [ -f web.pid ];
then
  echo Killing web
  kill $(cat web.pid)
  rm web.pid
fi

if [ -f api.pid ];
then
  echo Killing api
  kill $(cat api.pid)
  rm api.pid
fi
