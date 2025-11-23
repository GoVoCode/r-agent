#!/bin/bash

echo "Starting Restaurant Chat Agent Frontend..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
streamlit run frontend/app.py

