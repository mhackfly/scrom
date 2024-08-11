#!/bin/bash
NC='\033[0m'
YELLOW='\033[1;33m'
./scrom.sh
echo -e "${YELLOW}launching scrom.py...${NC}"
python3 scrom.py
