# Brewfather (brewfather.app) custom stream plugin for CraftBeerPi3

Use this plugin to send your fermentation temperatures to Brewfather stream

## Installation

Download and pull into the [craftbeerpi]/modules/plugins/ directory

Set the API Id from https://web.brewfather.app/#/tabs/settings/settings

## Updates

Temperatures will update every 15 minutes to Brewfather.

The fermenter must be active (running) for it to report readings to Brewfather.

You can attach the device (by fermenter name) to a batch under the Fermentation tab in Brewfather.

The sensors on the fermenter are reported to Brewfather as follows:

|SensorName|Brewfather Value|
|----------|----------------|
|Sensor|Temp|
|Sensor2|Fridge Temp|
|Sensor3|Room Temp|
