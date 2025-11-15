#!/bin/bash
# Quick article generation script for Unix/Mac
# Usage: ./quick_article.sh "Your Article Topic"

if [ -z "$1" ]; then
    echo "Usage: ./quick_article.sh \"Your Article Topic\""
    echo ""
    echo "Example: ./quick_article.sh \"Home Office Tax Deduction Guide\""
    exit 1
fi

python3 generate_article.py --topic "$1"
