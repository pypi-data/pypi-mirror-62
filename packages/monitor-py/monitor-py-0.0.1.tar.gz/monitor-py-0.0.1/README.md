# monitor.py

# Testing packaging

## v0.1 upcoming !

This is a small package to monitor server addresses by sending pings at desired intervals.  

Using a .json file to hold config options for the script.  The script will utilize logging and/or mqtt pub/sub.

Getting close to releasing v 0.1 of this which will have just basic functionality.  You will have to 
configure your .json config file manually.  In the next version there will be a script to aid in managing the config.

Planned for v0.2 :
* script to manage config options
* packaging of module
* testing
* verification of config (valid ip structure or if hostname that it is a valid hostname)

### Getting Started  
When the script scan.py is run, it will check for 3 directories and make them if they are not present :

`$HOME/monitor/`  
`$HOME/monitor/config/`  
`$HOME/monitor/logs`  

The project directory can be placed anywhere it will just place the log and config files in the appropriate
directories in the users home directory.

Log ouput will look like the following :


```    [DEBUG] [2020-02-29 14:54:54,897] : config file missing, creating default
       [INFO] [2020-02-29 14:54:54,904] : localhost is up...  
       [INFO] [2020-02-29 14:55:54,965] : localhost is up...  
       [INFO] [2020-02-29 14:56:55,014] : localhost is up...
```   

 localhost is the default server setup so you can immediately test if it is working.
