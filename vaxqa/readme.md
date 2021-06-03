# Vaccine Center Queue Analytics

## Requirements
1. Python 3.7+

## Installation
1. Setup a Python Virtual enviroment and install requirements.txt

<code>

    python3 -m venv env_vaxqa

    # unix based systems
    . env_vaxqa/bin/activate

    # windows
    env_vaxqa/scripts/activate.sh

    pip install -r requirements.txt
</code>

## Running the service to view dashboards
1. Switch to the <code> ./queue_analytics/ </code> folder and run <code> python intraday_queue_analytics.py </code>
2. Visit <code> 0.0.0.0:8100 </code> to view the dashboard.



