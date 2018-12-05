<h1>NEWS COLLECTOR</h1>

This project, written in Python 3, allows you to collect news articles from several online sources.

<h3>OVERVIEW</h3>

We use <a href="https://scrapy.org/">Scrapy</a>, an open source framework for extracting data from websites in a clean and 
scalable way. If you don't know about Scrapy, take a look at their <a href="https://doc.scrapy.org/en/latest/intro/tutorial.html">tutorial</a> to learn how to use it.


<h3>QUICK START</h3>

<h4>Install required Python libraries</h4>

You can easily install all the required libraries using pip:

```python
pip install -r requirements.txt
```

<h4>Create the MySQL database</h4>

To create the db you can use the db_creation.sql file.

Disclaimer: If you don't want to create a database, you can dump all the data
collected by this crawler to a json or csv file changing some simple code. Take 
a look at the Scrapy documentation for details.


<h4>Running the crawler script</h4>

Once you've installed all the required libraries and created the MySQL database with the
"feed_entries" table, you can run the crawler with the following command:

```python
python crawler.py
```
