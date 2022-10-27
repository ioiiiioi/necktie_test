
# Necktie

### Choice of framework and library
- i choose to use Django Rest Framework because :
    - it's very simple to create the new feature directory
    - have migration feature with no additional configs that can use as abstract model if we use legacy DB or as main models too
    - considerately lightweight framework
    - the library is already have the ORM
    - the configuration was almost ready to use

- the  drawback if we use Django Rest Framework are :
    - if we use the serializer for every data we create and update it will create multiple db transactions to insert/update and select, so i choose to use ORM with dataclass
    
- im assuming that, this app will deploy as microservices, i can use Flask or FastAPI but the configuration will take sometime to match up with django


### Potential improvement
- add kubernetes config file

### Product consideration
- to run the django test:
    - go to the root app dir on the terminal
    - type: `python manage.py test`
    
- to run docker-composer (presumably already in the app root dir):
    - type `docker-compose -p necktie -f deployment/docker-compose.yaml up --build -d`

### Assumption
- each doctor can have multiple service like as general practitioner and allergy and immunology
- each doctor can have multiple clinic hours in different hospital
- the services options are dynamic meaning, they can have new services or the services wasn't supported yet in this app
- in indonesia we have one district and split into multiple district, so i made the district models. usually we use government API to fetch the district/city/island/area-code data so we didn't need to update our data / code. 
