# Distributed Log Querier  

## Run unit tests
* On each server, run ```python generate_test_log.py``` to generate the test log file for that server
* Once the log files are generated, run ```python server.py``` on each server to start the server
* From any querying client, run ```python test.py```. This will run all 7 unit tests and output a report to the terminal.

## Run application
* Run ```python server.py``` on each server to start the server
* Run ```python client.py``` on any querying client, and type in your ```grep``` command at the prompt. The grep will print out all the lines matched, and in the end print out individual lines matched per file, and total number of lines matched.
* If any of the servers are down, the client program will print out which server could not be connected to.