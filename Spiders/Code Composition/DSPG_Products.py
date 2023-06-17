from enum import Enum

#This class is here so that we can expand to differnet products easier making the spider more dynamic and expandable
class Products(Enum):
    #Add products like this ProductName = index iteration, [], [] 
    #the 2 empty list will be filled in using the ProductsLoader class
    Bacon = 0, [], []
    Eggs = 1, [], []
    HeirloomTomatoes = 2, [], []

    # Helper method to reduce code for adding to the products and weed out duplicate inputs
    # if you type something in really wrong code will stop the setup is important 
    # correct index inputs are correct index number, url, urls, xpath, xpaths
    def addToProduct(self, items, index):
        product = None
        if isinstance(index, int):
            product = self.value[index]
        elif isinstance(index, str):
            if index.lower() in ['urls', 'url']:
                product = self.value[1]
            elif index.lower() in ['xpaths', 'xpath']:
                product = self.value[2]
        if product == None:
            raise ValueError(f"Invalid index input for ({index}) for input: {items}")
        #Sets are fast at finding dups so we use them for speed
        product_set = set(product)
        for item in items:
            if item not in product_set:
                product.append(item)
                product_set.add(item)