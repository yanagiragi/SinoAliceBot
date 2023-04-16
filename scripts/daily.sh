#!/bin/bash

TIMEOUT_INTERVAL=300

python main.py --debug true --routine "ProjectSekaiDaily" & sleep "${TIMEOUT_INTERVAL}" ; kill $!

python main.py --debug true --routine "HeavenBurnsRedDaily" & sleep "${TIMEOUT_INTERVAL}" ; kill $!