#!/bin/bash

# Variables
DB_NAME="College_DB"
DB_USER="postgres"
PYTHON_SCRIPT="postgre_creation.py"

# Function to check if PostgreSQL database exists and drop it if it does
drop_database_if_exists() {
    echo "Checking if database $DB_NAME exists..."

    DB_EXISTS=$(sudo -u $DB_USER psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME';" | grep -q 1)

    if [ $? -eq 0 ]; then
        echo "Database $DB_NAME exists. Dropping the database..."
        sudo -u $DB_USER dropdb $DB_NAME

        if [ $? -eq 0 ]; then
            echo "Database $DB_NAME dropped successfully."
        else
            echo "Failed to drop database $DB_NAME."
            exit 1
        fi
    else
        echo "Database $DB_NAME does not exist."
    fi
}

# Function to create PostgreSQL database
create_database() {
    echo "Creating database $DB_NAME..."
    sudo -u $DB_USER createdb $DB_NAME

    if [ $? -eq 0 ]; then
        echo "Database $DB_NAME created successfully!"
    else
        echo "Failed to create database $DB_NAME."
        exit 1
    fi
}

# Function to run the Python script for creating schema and inserting data
run_python_script() {
    echo "Running Python script to create schema and insert data..."
    python3 $PYTHON_SCRIPT

    if [ $? -eq 0 ]; then
        echo "Schema created and data inserted successfully!"
    else
        echo "Failed to create schema or insert data."
        exit 1
    fi
}

# Main execution

# Drop the database if it exists
drop_database_if_exists

# Create a new database
create_database

# Run the Python script to set up schema and insert data
run_python_script

echo "Script completed."
