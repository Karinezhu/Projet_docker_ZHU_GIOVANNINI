#! /bin/bash

mongoimport --host mongodb --database Bdt --collection grain --file /Dry_Bean_Dataset.csv --headerline --type csv

