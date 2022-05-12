# Vehicle Emissions Data Analyzer
## What is This Repo?
This repo contains the files to create and run kubernetes with a flask server contained inside that allows the user to analyze a dataset about the emissions of cars.
## What Data Does It Use?
The dataset can be found [here](https://www.kaggle.com/datasets/reubenowenwilliams/vehicle-emissions-dataset?resource=download), and the raw data can be found [here](https://raw.githubusercontent.com/ReubenGitHub/ML-Vehicle-Emissions/main/data/processed/uk_gov_data_dense_preproc.csv).
## How Start it Up!
To use the application, first pull the repository to your own machine. Then (I DONT KNOW THE EXACT PROCESS USED TO SET UP THE k8s) Next you will need to run the Makefile. To do this, execute `make upd-all` within your terminal. This command will delete the old containers, build new containers, run the new containers, and push them to the docker hub. After running the Makefile, you should be good to start curling the flask server!
## Curling the Flask Server!
There are many curl endpoints that you can use to interact with the data, lets go through each of them and what they do.
1. The first endpoint that you must curl is /reset. To do this, execute `curl https://isp-proxy.tacc.utexas.edu/geovbra-1/reset -X POST`. This will reset the data and push it to the redis database.
2. The next endpoint to curl is the "help" endpoint. To do this execute `curl https://isp-proxy.tacc.utexas.edu/geovbra-1/`. This will list all of the available curl endpoints like this:


   

     How to use our Vehicle Emissions Analyzer
        
        Step 1:
        Reset the data in the kubernetes database by running a curl request with endpoint /reset -X POST
        
        Step 2:
        Every part of CRUD is available. For instructions on how to use each route, use:
            /create
            /read
            /update
            /delete
            /jobs
3. Using the same format as the "help" endpoint above, you can call each of these CRUD endpoints to get an in depth explanation on how to use them and what they do. For example, executing `curl https://isp-proxy.tacc.utexas.edu/geovbra-1/read` will return :


```
How to use /read:
   
Syntax:
/read/KEY?start=VALUE with the capital words being user inputs


What the inputs can be:

KEY:
    all - returns all of the stored data
    car_id - returns all data with specified car_id
    manufacturer - returns all data with specified manufacturer
    model - returns all data with specified model
    description - returns all data with specified description
    transmission - returns all data with specified transmission
    transmission_type - returns all data with specified transmission_type
    engine_size_cm3 - returns all data with specified engine_size_cm3
    fuel - returns all data with specified fuel
    powertrain - returns all data with specified powertrain
    powertrain_ps - returns all data with specified powertrain_ps
    co2_emissions_gPERkm - returns all data with specified co2_emissions_gPERkm


VALUE:
    Using the read/all route, find a value for your field that you would like to evaluate (IE: read/manufacturer?start=MERCEDES-BENZ)
```
The same is true for /create, /update, /delete, and /jobs.

4. Each of the CRUD functions only deal with reading and altering data within the redis database itself, however, the /jobs route will analyze two fields within the dataset given by user input. It then returns a png that the user can download which depicts either a bar graph or a scatterplot of the two fields with one being the x-axis and the other being the y-axis. When calling the download route, the png will be stored in the current directory that the user's terminal is in adn can be easily opened in the local computer's file explorer.
