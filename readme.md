# Vaccine Appointment Booking system

## Requirements
1. Python 3.7+
2. Matlab 2021
   1. YALMIP
   2. Mosek
3. MS Excel (xlsx support)

## Installation
1. Setup a Python Virtual enviroment and install requirements.txt

<code>

    python3 -m venv env_appt_booking

    # unix based systems
    . env_appt_booking/bin/activate

    # windows
    env_appt_booking/scripts/activate.sh

    pip install -r requirements.txt
</code>

2. Within the virtualenv follow instructions for installing matlab.engine library. ref. https://www.mathworks.com/help/matlab/matlab-engine-for-python.html

## Database Setup


## Running the service to view dashboards
1. Switch to the <code> ./vaccine_appointment_system/utility_simulator/ </code> folder and run <code> python index.sh </code>
2. Visit <code> 0.0.0.0:8050 </code> to view the dashboard.
3. The <code> ./results/ </code> folder contains a set of scenarios that can be visualised in the dasboard.

## Running the service to evaluate / execute new Scenarios
1. Follow the instructions in previous section to start the dashboard
2. In a new shell run <code> python process_excel_server.py </code>
   - NOTE: Any excel file placed in the <code> ./inputs/excel/ </code> folder will be executed immediately.
3. Samples of excel scenario descriptors are in the <code> ./examples/ </code> folder
   - NOTE: the scenarios should be carefully constructed and all the column headers and row headers are case sensitive. Also at this moment, only 70 Day lookahead with fortnightly 5 wave invitations are supported.
4. Upload the scenario via the webservice (Upload Scenario Tab).
5. scenario status can be viewed in the same page and when status changes to 'Completed', the dashboard for that scenario is ready for viewing.


