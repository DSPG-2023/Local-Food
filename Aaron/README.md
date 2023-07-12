
# Spider Folder
This is the spider folder home to all the spiders that I've built during the summer of 2023 as a part of DSPG. 

## Warning 
The contents of each file were made for the DSPG AI/Local foods project. These files are intended to stay within the scope of the project. Modifications to expand outside the scope of the project is not recommended and is VERY discouraged. 

It is crucial to note that each of these spiders can potentially be rendered non-functional in the future. Any modifications or changes made to the websites can result in the program breaking, leading to the need for extensive repairs and modifications to the spiders. 

### Requirements
There are two python packages that are required. 
``` 
pip install selenium
pip install scrapy
```
The web browser Firefox is also required. ( Note: You can modify the selenium spiders to work with Safari or Chrome however it is highly recommended to use Firefox )

Strong reliable internet and a fast computer is also recommended.

### Spiders Built for the Following Websites:
1. Fresh Thyme
2. Hy-Vee
3. Gateway Market
4. New Pioneer Co-op
5. Russ's Market
6. Iowa Food Hub
7. Joia Food Farm

### How to Run a Spider

While each spider differs in terms of its structure and creation process, they all follow a similar process when it comes to running them. Each spider is conveniently build in a Jupiter notebook in python. In VSCode you can simply click the run all button at the top and the spider will work its magic. 

The speed of each spider varies, so the time it takes to run can range anywhere from a minute to around 30 or more. The spider's runtime is determined by the amount of scraping it needs to perform. The more scraping it has to do, the longer it will take to complete.

Once you've run all the spiders there’s DSPG_DataManager that you can run. It will combine each of the spiders outputs into a master product CSV file.

### Adding products

This process is quite streamlined and does not require you to do too much. You will need to follow the implemented format.

1. DSPG_Products.py 
    - Products() -> loadProducts() -> ProductList
        - Add [Increamt Index, 'Product Name']
        - You will need to remember this index number 

    - Products() -> dataFrameAdder() -> ProductDataFrames
        - Add the columns here.

2. DSPG_Cleaner.py
    - DataCleaner() -> LoadDataSet() 
        - Add to the elif with the index number
    - You may want to add a Modification function for this new product

3. In each spider
    - For Selenium spiders
        - ProductsLoader() -> urlsAdder()
            - Add a list with the urls of the product
            - Add self.Products[index number].append( Your URL List )
        - ProductsLoader() -> xpathMaker()
            - Check the xpaths. Sometimes you may want to change or add to this. Its important to follow the format and add to the xpath list. 
            - This is where you want to think about passing in any extra values to your Modification function if need be.
            - In the example folder there is a TestingXpaths.ipynb which have a few examples of how to test for xpaths.
            - Add self.Products[index number].append( xpath List )
        - DataFormater() -> cleanUp() 
            - Add to the elif with the index number. You will need to call the Modification function inside this.

    - For Scrapy Spiders
        - start_requests()
            - this is were you will add the URL
        - Each spider is a bit different so you will have to expand upon the class and understand whats going on. There are some examples that have comments to help you add products. 

4. DSPG_Branding 
    - You will need to modify and add the brands to the following list with this format.
        - getLocalBrands  
            -No spaces or special characters only lowercase letters
        - getNonLocalBrands 
            -No spaces or special characters only lowercase letters
        - getBrandNames 
            - first character is capital the rest is lower case
            - special characters allowed (', ,-,&)
    - There are two functions to help you with formating at the bottom.

5. The new product is added! 
    - Run each spider to see if you implemented the new product correctly.
        - **Tip**: Comment out the other products urls like this.
        ``` python
        ProductUrls = [
                        # www.example/1.com
                        # www.example/2.com
                      ]
        ```
    - Run DSPG_DataManager to see if you added all the brands it correctly

### What to do if you have a skip
Run the spider again

### Improvements 

There are numerous improvements that can be made to enhance the overall performance, efficiency, and scalability of each of these spiders. However, it is important to note that implementing these improvements may require more time and resources than what is currently available. 

One notable improvement worth mentioning is in the Hyvee spider. If you are able to set the store location before scraping the products a large gap of data would be filled.  

#### Selenium spiders Improvements
- Add threading to the Selenium spider code. This could be added when the spider go through each of the xpaths. 

- Improvements the skip handler in each selenium spiders. I wasn't able to fully test this aspect so there may be some bugs. 

#### Scrapy spiders

- Adding a spider logger similar to the selenium spider

#### General Improvements

- Going through each of the spiders website URLs and seeing if there is anything more we can extract.

- Add a method that calls and runs every spider class. This is not worth spend a lot of time in doing until improvements the skip handler in each selenium spiders is made. Running each of the spiders manually works and is easy to look over.

- Improve the process of new products

- Improve the process of adding brands 

### Experimentation
Experiment by Move the cleaning processes out of the spider entirely. 
One experiment that is definitely worth trying is making use of the package Scrapy splash. It is an extension to scrapy which could replace all the selenium spiders. In my research of spiders I found that Scrapy Splash is generally faster then Selenium. Meaning the speed of scraping process could be improved dramatically. I did not have enough time to dive into this and get this to work. So if the time is available it is definitely worth exploring this.

In the selenium spiders. I when was adding products to each of spiders. I when to the store page and manually clicked each of the products and saved the link into the spider. There is a few issue with this:

1. We don't know if any new products are added to the cite.
2. We don't know if the product is gone. 

For some of the spiders it can handle if a product is not found. By either explicitly saying that is not in stock or skipping the URL.  However each time we run into this case it will slow the spider down.
To fix this we add the URL that contains the table of all the products with the necessary product requirements then go through each of the table's product cards in a new page. From there it will be scraping process. This process already implemented in the scrapy spiders. This will make the spider **much** slower and is the reason I didn't do this because I did not have the time. However for the longevity of the project it is worth it.

In the selenium spiders you could make it so that opens more URLs at a time instead of one by one. This will require a strong computer to run the code however it could drastically improve runtime. You would need to increase the wait time for it load the pages however. An example could be one product per page.

# Diagram Folder
This contains Diagrams of the spider implementation.

# Data Folder
This contains data collected from the spider.

# AI Housing Folder
This contains a spider I built for the AI Housing team. Note this spider needs work as it does not function to the fullest.
