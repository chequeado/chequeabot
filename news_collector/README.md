<h1>NEWS COLLECTOR</h1>

This project, written in Python 3, allows you to collect news articles from several online sources.


<h2>OVERVIEW</h2>

We use <a href="https://scrapy.org/">Scrapy</a>, an open source framework for extracting data from websites in a clean and 
scalable way. If you don't know about Scrapy, take a look at their <a href="https://doc.scrapy.org/en/latest/intro/tutorial.html">tutorial</a> to learn how to use it.


<h2>QUICK START</h2>


<h3>Install required Python libraries</h3>

You can easily install all the required libraries using pip:

```python
pip install -r requirements.txt
```

<h3>Create the MySQL database</h3>

You will need a database to dump all the articles collected. To create it you can use the <b>db_creation.sql</B> file.
Once you created your database, update the <b>credentials.py.example</b> with your database crendetials and change the file name to <b>credentials.py</b>

<i>Disclaimer: If you don't want to create a database, you can dump all the data
collected by this crawler to a json or csv file changing some simple code. Take 
a look at the Scrapy documentation for details.</i>


<h3> Setup your own spiders </h3>

We have uploaded some of our custom spiders to provide examples, but if you want to add your own sites you will need to create your own spiders.
The work of a spider is splited in two parts. First, it must collect all the articles links from a specific section of a news-site. We call this the <i>parse section</i> stage. After that, the spider will travel to each link and extract the article from there. This is the <i>parse article</i> stage.


<h4>Parse SECTION function</h4>


If the news-site we are scraping has RSS feed, the parse section code will look like this:

```python
    def parse_seccion(self, response):
        feed = feedparser.parse(response.url)
        for entry in feed['entries']:
            request = scrapy.Request(url=entry['link'], callback=self.parse_noticia)
            request.meta['item'] = entry           
            yield request
```

If RSS is not available we will use xPath to extract those links:

```python
    def parse_seccion(self, response):
        # This path goes after each @href inside the summary-news-list of a specific site.
        # This is relative to each site and you will have to inspect the html of the site to know were to look.
        noticias = set(response.xpath('//div[@class="summary-news-list"]/article/header/h1/a/@href').extract())
        for noticia in noticias:
            yield scrapy.Request(url=noticia, callback=self.parse_noticia)
```



<h4> Parse ARTICLE function </h4>

For this stage we also have two options. The first one uses <a href="https://newspaper.readthedocs.io/en/latest/">Newspaper library</a> to automatically extract the article title, content, date and autor. This option is very easy to implement and doesn't require any tweaking.

```python
    def parse_noticia(self, response):
        ff = newspaper.Article(response.url)
        ff.download()
        ff.parse()
        data = {
            'titulo': ff.title,
            'fecha':  datetime.datetime.now(),
            'noticia_texto': ff.text,
            'noticia_url': ff.url,
            'source': 'news_site_name',
            'formato': 'web'
        }
        yield data
```

To know if it works you should run the crawler and see if it scrapes correctly the articles content.
If it doesn't, you will have to tweak this code a little bit and use xPath instead of Newspaper.
Example:

```python
    def parse_noticia(self, response):
        raw_date =  response.xpath('//p[@class="news-body-paragraph paragraph-date"]/text()').extract()[0]
        formated_date = datetime.datetime.strptime(fecha_texto.split('-')[1].strip(), '%A  %d de %B de %Y')
        body = ' '.join([e for e in response.xpath('//div[@id="note-body"]/p/text()').extract()])
        title = response.xpath('//h1[@class="news-header-title"]/text()').extract()[0]
        
        data = {
            'titulo': title,
            'fecha': formated_date,
            'noticia_texto': body,
            'noticia_url': response.url,
            'source': 'La Capital',
            'formato': 'web'
        }

        yield data
```

<b>Examples of spiders implementation can be found in the <i>spiders</i> folder. Check to see which of our spiders fits better in your site.</b>

Spiders that are going to crawl are detailed in the <i>TO_CRAWL</i> list in <i>crawlers.py</i>.


<h3>Running the crawler script</h3>

Once you've installed all the required libraries, created the MySQL database with the
"feed_entries" table, and set up your spider, you can run the crawler with the following command:

```python
python crawler.py
```
