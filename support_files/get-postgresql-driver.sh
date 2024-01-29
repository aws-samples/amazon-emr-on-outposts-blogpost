#!/bin/bash
sudo mkdir -p /opt/spark/postgresql/driver
cd /opt/spark/postgresql/driver

n=0
while [ ! -f postgresql-42.6.0.jar ]; do
    sudo aws s3 cp s3://blog-emr-on-outposts/postgresql-42.6.0.jar .
    n=$[$n+1]
    [ $n -ge 60 ] && break
    sleep 5
done
