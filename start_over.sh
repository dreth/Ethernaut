#!/bin/bash

echo 'Cleaning up...'
rm ./scripts/*.py
rm ./reports/*.md
rm ./contracts/attacks/*.sol
rm ./contracts/attacks/*.yul
rm -rf ./.vscode
echo 'Done!'
