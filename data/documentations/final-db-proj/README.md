# Final Database Course Project - Fall 2020

An application for managing a database and do CRUD operations on its different tables.

The schema is derieved from first exercise which was to create ER model for an online airline ticket booking website and it is available in folder ```sql``` which also has queries for creating tables and inserting some records in it.

One of the advantages is you can add or remove columns from the schema only by changing the schema itself and making those changes in ```config.yml``` and ```object.py``` and the program will be adopted to that change itself.

## Operations
Inserting is straightforward but for deleting and updating, at first you must select a row or cell respectively and then click the button. After that, you must see that change or an dialog box in case the query could not be committed.

Optional box is embedded for you to see anything from the tables you want and you will see the results in an informative dialog box.

Here you can see a sample of each window and different operations:

<p align="center">
<img src="./screenshots/1.png">
<img src="./screenshots/2.png">
<img src="./screenshots/3.png">
<img src="./screenshots/4.png">
<img src="./screenshots/5.png">
<img src="./screenshots/6.png">
<img src="./screenshots/7.png">
<img src="./screenshots/8.png">
<img src="./screenshots/9.png">
<img src="./screenshots/10.png">
<img src="./screenshots/11.png">
<img src="./screenshots/12.png">
<img src="./screenshots/13.png">






</p>

## More
You can switch between dark and light them only by changing `if True` to `False` in the beginning of `gui/darkTheme.py`.
