#!/bin/bash

docker build ./backend/ -t joachimveulemans/license-plate-reader:backend

docker build ./frontend/ -t joachimveulemans/license-plate-reader:frontend
