# OKTA-CTL

## Installation
The easiest way to install `oktactl` is to use pip in a virtualenv:  
  
  
```
$ pip install oktactl  
```  

## Getting started
  
  
Before using `oktactl`, you need to tell it about your okta credentials.   
    
The quickest way to get started is to run the oktactl configure command:  
```
$ oktactl configure
Domain name: foo
API token: bar
```
    
      
### List of available commands:  
   * [list-users](#list-users)
   * [create-user](#create-user)
   * [create-groups-and-assign-to-app](#create-groups-and-assign-to-app)
   * [delete-groups](#delete-groups)
  
   
#### list-users:  
   - Used to list all the users under an account:
      - Parameters: `None`    
      - Options: `None`    
#### create-user:  
   - Used to create an user:  
      - Parameters:  
            `--first-name TEXT  User's first name`  
            `--last-name TEXT   User's last name`  
            `--email TEXT       User's email id`  
            `--login TEXT       User's login id`  
            `--number TEXT      User's phone number`  
            `--password TEXT    User's password`  
      - Options:  
            `User's first name:`   
            `User's last name:`   
            `User's email id:`   
            `User's login id:`   
            `User's phone number:`   
            `User's password:`   
#### create-groups-and-assign-to-app:  
   - Used to create multiple groups and assign them to one app based on the app id:
      - Parameters: `None`
      - Options:  
          - Option 1: Provide inputs manually
          - Option 2: Read through CSV file
              - Option 1:  
                  `Group name:`  
                  `Group Description:`  
                  `Do you want create one more group? [y/N]:`  
                  `App id:`  
              - Option 2:  
                  `Path of CSV file:`   
                  `App id:`   
                  
#### delete-groups:
   - Used to delete all groups present in an account except the default group
      - Parameters: `None`    
      - Options: `None`  
