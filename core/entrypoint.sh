#!/bin/sh

 
# Run Alembic migrations
echo "Running Alembic upgrade to head"
python -m alembic upgrade head

"$@"