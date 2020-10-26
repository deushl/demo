# Fullstack project demo

## How to get the project up and running

First and foremost, please provide a valid personal github token in the file env.py located at demo/env.py, otherwise the project will run with the limitations of the anonymous github API.

To get the project up and running, you need python 3 and pip, first install the python dependencies using `pip3 install -r requirements.txt`.

Next please run `python3 manage.py makemigrations` and `python3 manage.py migrate`. Once the migrations are completed, to fetch all the data from the Github API, you need to run `python3 manage.py refreshrepos`, this is a custom command that will initiate the data fetch.

Alternatively I have provided a dockerfile, in the project, the only thing you need to run to set the project up this way is `docker build -t demo .` and `docker run -p 8000:8000 demo`. 

## Future Improvements
I would like to clean the ingestion code, since it is a little bit slopy, maybe add multithread support to make the process faster than it is now (currently takes arount 40 seconds to ingest the data).
