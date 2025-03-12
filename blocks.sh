#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Usage: $0 <wallet_name>"
  exit 1
fi

WALLET_NAME="$1"

# Создаем кошелек
echo "Creating wallet '$WALLET_NAME'..."
./src/cyberyen-cli -regtest createwallet "$WALLET_NAME"

# Получаем новый адрес
echo "Generating new address..."
NEW_ADDRESS=$(./src/cyberyen-cli -regtest getnewaddress)

# Генерируем блоки
echo "Generating 432 blocks to address $NEW_ADDRESS..."
./src/cyberyen-cli -regtest generatetoaddress 432 "$NEW_ADDRESS"

echo "Done!"
