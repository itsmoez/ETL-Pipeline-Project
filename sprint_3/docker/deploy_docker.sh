#!/bin/bash

#check if docker is running 
if ! docker info > /dev/null 2>&1; then # check if docker desktop is running
  echo "Docker not running. Attempting to run Docker now..." #let user know docker is not running 
  sleep 5 
  "C:/Program Files/Docker/Docker/Docker Desktop.exe" #start docker desktop
  echo "Docker is booting!" #confirms docker is starting
  sleep 15 #delay for 15 seconds so docker has time to boot
elif docker info > /dev/null 2>&1; then
  echo "Docker is running!" #confirms Docker is running
  docker ps
else
  echo "An unexpected error occurred." #otherwise if there are any issues it echo's an error message
fi


echo "Starting Docker containers now..." #confirms the next step is starting

#docker-compose -f docker-compose-group.yml down #when changes are made to the containers need to get rid of the old ones 

docker-compose -f docker-compose-group-v2.yml up #builds the container and network

#to run the bash script first you need to be in the correct directory before running the command below 
# run the following command in your powershell terminal ./docker_script.sh or bash docker_script.sh in a git bash terminal. 
