# Lokly the Indian Address Parser 

Addresses often provide a significant amount of intelligence about the buying and spending habits of a consumer.  In most cases this intelligence cannot be determined from the address as most of the addresses are free flowing text and are not easily parsed.  Faced with these challenges we have created an address parser exclusively for Indian addresses. Lokly the Indian address parser helps you parse an address contained in a free flowing string.  Divide a single address (as string) into separate component parts : house number, street type (bd, street, ..), street name, unit (apt, batiment, ...), zipcode, state, country, city etc. 

Soon we would be adding intelligence around the neighborhoods to help you determine the economic value of the addresses. 

# What is parser based on?  

The parser is based on natural language processing, parsing technology, and text mining. 

# How to test it 

You can test it at www.lokly.in.   This is currently in beta and is available for anyone to use and modify for their use. 

# Installation 

```bash
#Clone the repository
git clone https://github.com/spandansingh/url_scraper.git
```

```bash
#Build the image
sudo docker build -t 99roomz/lokly .
```

```bash
#Run the container
sudo docker run -d -t -i -e email='<email>' -e password='<password>' -p 80:80 --name lokly 99roomz/lokly
```

Yay! Everything is now up and running.

# How to contribute 

Want to file a bug, contribute some code, or improve documentation? Excellent! Send a mail to hello@lokly.in. 

# License 

Code is MIT Licensed
