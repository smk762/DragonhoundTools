#!/bin/bash

git config --file=../.gitmodules submodule.notary/dPoW.branch dev
git submodule update --remote

