#!/bin/bash


ssh-keyscan -H kate.pbuttergirl.com >> ~/.ssh/known_hosts
eval "$(ssh-agent -s)"
chmod 600 deployment/deployment.key
ssh-add deployment/deployment.key

git remote add dokku dokku@kate.pbuttergirl.com:tesco
git push dokku master