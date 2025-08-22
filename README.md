# Currency Tracker

An end-to-end data fetch and analysis pipeline for Euro conversion rates from the European Central Bank.
The purpose of the application is to feed a dashboard that makes it easy to see
the latest trends in conversion rate from the euro to foreign currencies.

The application addresses the questions:

* What is the current exchange rate?
* What is the recent trend in the exchange rate?
* How does the current exchange rate compare to historical rates?

## Overview

The `analysis` directory contains a Python Jupyter notebook with exploratory
analysis results on an example European Central Bank conversion rate dataset. It
checks completeness and viability of the data.

The `app` directory contains the application to pull, store, and visualize the data.

The application consists of three components packaged into their own Docker
containers:

1. **upload**: Python script that pulls the latest data from the ECB website
and adds it to the PostgreSQL database.
1. **database**: PostgreSQL database that stores conversion rate data.
1. **dashboard**: Plotly Dash that visualizes conversion rate data.

## Prerequisites

1. Install Docker CLI and Colima 
1. Copy `app/.env.example` to `app/.env` and fill in the missing fields. The ssh key
path and host name are only required if deploying to a remote server using the
deploy.sh script.

Optional: To deploy the application to a server, download the private key file
and fill in its directory location in the .env file.

## Usage

The code in `app` can be run using `make` commands defined in `app/Makefile`.

To run the application locally: `make dev`

The Plotly dashboard will be visible from your browser on `localhost:8050`

To stop and remove containers: `make down`

To deploy the application to a remote server via `scp`: `make deploy`

Once deployed to the server, the upload job is configured to run at 22:00 UTC
Monday - Friday to pull the latest data from the ECB. Note the deploy script
overwrites any existing cron jobs scheduled on the server.