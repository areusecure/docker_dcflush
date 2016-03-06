# docker_dcflush
Ever been frustrated by the fact that you named some docker-container "db" a couple of hundred Docker-containers back? 
I wrote this utility to get rid of all those dead containers to free up available container names. 
Activity is logged to ./docker_dcflush.log

MIT-license, use at your own risk.
To complete the flush, restart the docker daemon after running docker_dcflush.py.

python docker_dcflush.py
