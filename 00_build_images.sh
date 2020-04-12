#!/bin/bash

docker build ./backend/ -t license-plate-reader:backend

docker build ./frontend/ -t license-plate-reader:frontend
