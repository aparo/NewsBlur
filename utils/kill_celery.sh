#!/bin/sh

ps aux | grep celeryd | egrep -v grep | awk '{print $2}' | xargs kill -9