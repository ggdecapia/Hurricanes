# Extract-Transform-Load Challenge Instructions V1.0
## Written by Christopher Sadlo and Glenda Decapia

<br><br>

# Step 1
### Clone the repository:

* Launch Git BASH or your favorite terminal.

* Move into the directory you want to store the package


        cd <my_directory>
        git clone https://www.github.com/csadlo/Hurricanes


# Step 2
### Installing the country_converter API:  https://pypi.org/project/country-converter/

    source activate NewPythonData
    pip install country_converter --upgrade
    cd Hurricanes


# Step 3
### Creating api_keys.py file:

* Create a file called "api_keys.py" in the ETL-challenge folder and add the following code:

        weather_api_key = "<insert your api key for OpenWeatherMaps.org>"
        google_key = "<insert your api key for Google Maps>"

* Save and close the api_keys.py file in the Project 2/Hurricanes root folder.


# Step 4
### Creating config.py file:

* Create a file called "config.py" in the Project 2/Hurricanes folder and add the following code:

        username = "<insert your username>"
        password = "<insert your password>"

* Save and close the config.py file in the Project 2/Hurricanes root folder.


# Step 5
### Launching and setting up the hurricanes database in pgAdmin:

* Launch pgAdmin.
* Right-click on "Databases" and create a new database called "hurricanes".
* Right-click on "hurricanes" and left-click on "query-tool".
* Click on the open file icon and navigate to the Project 2/Hurricanes folder.
* Open the "schema.sql" file.
* Run the schema.sql file to create the table.


# Step 6
### Executing the jupyter notebook:

* Move into the Project 2/Hurricanes folder if not there already.

        cd Hurricanes
        jupyter notebook

* Open and execute hurricane.ipynb file

# Step 7

* Return to the pgAdmin tab in your browser
* Databases -> hurricanes -> schemas -> public -> Table -> hurricanes
* Now either right-click on hurricanes 
    -or-
* Highlight hurricanes and select "Object" in the top tool bar and then click "Properties"
* A window will pop-up. Select the "Columns" tab.
* From there, while looking at the "index" row, toggle the "Not NULL?" and "Primary Key?" options to "yes"
* SAVE