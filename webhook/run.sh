#!/bin/bash
. ../Aplicação/keys.py
chmod u+x ngrok
./ngrok authtoken $NGROK_KEY
./ngrok http 8080
