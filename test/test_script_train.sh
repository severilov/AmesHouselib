#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

test_exit_code () {
  if [[ $? = 0 ]]; then
      echo -e "${1} - ${GREEN}OK${NC}"
  else
      echo -e "${1} - ${RED}FAILED${NC}"
      cat log.txt
      exit 1
  fi
}


python ./src/scripts/train.py &>log.txt
test_exit_code train