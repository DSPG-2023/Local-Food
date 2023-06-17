from DSPG_Products import Products #Imports the products

#This is a helper class to reduce duplicate code in the DataCleaner class
class DataSanitizer():
    def cleanPricing(self):
        price = ''.join(c for c in self.Data['Current Price'] if c.isdigit() or c == '.')
        if len(price) == 0:
            return
        self.Data['Current Price'] = float(price)
        if self.Data['Orignal Price'] == None:
            self.Data['Orignal Price'] = self.Data['Current Price']
            return
        price = ''.join(c for c in self.Data['Orignal Price'] if c.isdigit() or c == '.')
        if len(price) == 0:
            self.Data['Orignal Price'] = self.Data['Current Price']
        else:
            self.Data['Orignal Price'] = float(price)
        
    def ozToLb(self, input):
        weight = str(input).lower()
        if 'oz' in weight:
            return self.stringValueExtraction(weight, 'oz') / 16.0
        elif '/lb' in weight:
            value = self.stringValueExtraction(weight, '/lb')
            if value == None:
                return 1.0
            return value
        elif 'lb' in weight:
            return self.stringValueExtraction(weight, 'lb')
        return weight
    
    #Helper to reduce code. Splits the string and returns the float value 
    def stringValueExtraction(self, string, stringType):
        value = ''.join(filter(lambda x: x.isdigit() or x == '.', string.split(stringType)[0]))
        if(len(value) == 0):
            return None
        return float(value)

    def determineLocality(self):
        localBrands = None
        nonlocalBrands = None
        #For speed we use sets and turn everyting to lowercase and no spaces for accuracy
        if(self.productType == Products.Bacon.name):
            #This is for read ability 
            #['dm bacon co', 'des moines bacon co.', 'webster city', 'berkwood farms', 'berkwood farms', 'berkwood farms', 'berkwood farms', 'berkwood farms', 'de bruin ranch']
            #['niman ranch', 'jolly posh', 'nueske', 'niman ranch']
            localBrands = {'dmbaconco', 'desmoinesbaconco.', 'webstercity', 'berkwoodfarms', 'berkwoodfarms', 'berkwoodfarms', 'berkwoodfarms', 'berkwoodfarms', 'debruinranch'}
            nonlocalBrands = {'nimanranch', 'jollyposh', 'nueske', 'nimanranch'}
        elif(self.productType == Products.Eggs.name):
            localBrands = {}
            nonlocalBrands ={}
        elif(self.productType == Products.HeirloomTomatoes.name):
            localBrands = {}
            nonlocalBrands ={}    
            #Sometimes it says it the name 
            if 'local' in self.Data['Product Type'].lower().replace(' ', ''): # convert to lowercase and remove spaces
                self.Data['Local'] = 'Local'
                return
        #Add product brands here
        else:
            #Catch if no brands are set for the product
            return 
        if self.Data['Brand'] == None:
            #If no brand was set we look at the product name
            brand = self.Data['Product Type']
        else:
            brand = self.Data['Brand'].lower().replace(' ', '')
        if brand in localBrands:
            self.Data['Local'] = "Local"
        elif brand in nonlocalBrands:
            self.Data['Local'] = "Non-local"
        else:
           self.Data['Local'] = "None Listed"
