#!/bin/bash

if [ "$1" == "local" ]; then
  INSTALL_PATH="~/bin"
else
  INSTALL_PATH="/usr/local/bin"
fi

if [ "$1" == "remove" ] || [ "$2" == "remove" ]; then
  echo "Removing files from $INSTALL_PATH"
  rm $INSTALL_PATH/makefile.py
  rm $INSTALL_PATH/makefilecc.py
  rm $INSTALL_PATH/pymake
else
  echo "Copying files to $INSTALL_PATH"
  cp makefile.py $INSTALL_PATH
  cp makefilecc.py $INSTALL_PATH
  cp profiles.py $INSTALL_PATH
  cp pymake $INSTALL_PATH
  chmod +x $INSTALL_PATH/pymake
fi
