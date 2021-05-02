# JOBSCRAP

Jobstreet Scrapping Application

# How to build docker image

From jobscrap directory run:

`docker build -t jobscrap .`

`docker run jobscrap`

After you run the docker image, it will automatically scrape data from jobstreet and store it to database (in this case mongodb)

![docker run](assets/docker_run.png?raw=true)
