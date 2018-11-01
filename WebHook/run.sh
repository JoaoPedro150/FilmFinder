#!/bin/bash
. ../Aplicação/config.py
chmod u+x ngrok
./ngrok authtoken $NGROK_TOKEN
./ngrok http 8080
