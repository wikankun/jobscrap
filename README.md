# JOBSCRAP

Jobstreet Scrapping Application

# How to build docker image

From jobscrap directory run:

`docker build -t jobscrap .`

`docker run jobscrap`

After you run the docker image, it will automatically scrape data from jobstreet and store it to database (in this case mongodb)

![docker run](assets/docker_run.png?raw=true)

If you want to get all the scrapped data out of database, open this url:

[Get all scrapped data](https://jobstreetscrap-api.herokuapp.com/jobs/?apiKey=1234567asdfgh)

Anyway, here's a screenshot of my mongodb atlas dashboard:

![mongodb atlas dashboard](assets/mongodb_atlas.png?raw=true)

