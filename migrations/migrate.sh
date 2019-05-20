#!/bin/bash

export PGPASSWORD=postgres
psql -U postgres -h localhost -d postgres -f tables.sql
