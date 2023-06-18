from DSPG_Products import Products #Imports the products
from DSPG_SpiderErrors import DataCleanerError
from DSPG_SpiderErrors import BrandingError
from datetime import datetime

#This is a helper class to reduce duplicate code in the DataCleaner class
class DataCleaner():
    def LoadDataSet(self, inputIndex, url):
        self.productIndex = inputIndex
        if inputIndex == 0:
            self.Data = {'Product Type': None,
                         'Current Price': None,
                         'Orignal Price': None,
                         'Weight in lbs': None,
                         'True Weight': None,
                         'Brand': None,
                         'Local': None,
                         'Address': None,
                         'State': None, 
                         'City': None, 
                         'Zip Code': None, 
                         'Date Collected': str(datetime(datetime.today().year, datetime.today().month, datetime.today().day))[:-9], 
                         'Url': url
                        }
        elif inputIndex == 1:
            self.Data = {'Product Type': None,
                         'Current Price': None,
                         'Orignal Price': None,
                         'Amount in dz': None,
                         'True Amount': None,
                         'Brand': None,
                         'Local': None,
                         'Address': None,
                         'State': None, 
                         'City': None, 
                         'Zip Code': None, 
                         'Date Collected': str(datetime(datetime.today().year, datetime.today().month, datetime.today().day))[:-9], 
                         'Url': url
                        }
        elif inputIndex == 2:
            self.Data = {'Product Type': None,
                         'Current Price': None,
                         'Orignal Price': None,
                         'Weight in lbs': None,
                         'True Weight': None,
                         'Brand': None,
                         'Organic': None,
                         'Local': None,
                         'Address': None,
                         'State': None, 
                         'City': None, 
                         'Zip Code': None, 
                         'Date Collected': str(datetime(datetime.today().year, datetime.today().month, datetime.today().day))[:-9], 
                         'Url': url
                        }
        else:
            raise DataCleanerError(inputIndex)
            
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
    
    def baconModifications(self):
        #Finds True Weight if not available 
        if(self.Data['True Weight'] == None):
            self.Data['True Weight'] = self.findWeight()
        #Sets the Weight in lbs if possible
        if(self.Data['True Weight'] != None):
            self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])

    def ozToLb(self, input):
        if input == None:
            return None
        weight = str(input).lower()
        if 'oz' in weight:
            return self.stringValueExtraction(weight, 'oz') / 16.0
        elif '/lb' in weight:
            return 1.0
        elif 'lb' in weight:
            return self.stringValueExtraction(weight, 'lb')
        return None

    #If no weight is given we look at other places that could have what we need
    #This Determines if a list talking about weights in ounces or pounds.
    def findWeight(self):
        #Checking these places for clues
        checkLocations = [self.Data['Current Price'], self.Data['Product Type'], self.Data['Orignal Price']]
        possible = []
        for string in checkLocations:
            if string == None:
                continue
            string = string.lower().replace(' ', '') # convert to lowercase and remove spaces
            if 'pound' in string:
                return  f"{self.stringValueExtraction(string, 'pound')} lb"
            elif 'ounce' in string:
                return f"{self.stringValueExtraction(string, 'ounce')} oz"
            elif '/lb' in string:
                return f"{self.stringValueExtraction(string, '/lb')}/lb"
            elif 'lb' in string:
                return f"{self.stringValueExtraction(string, 'lb')} lb"
            elif 'oz' in string:
                return f"{self.stringValueExtraction(string, 'oz')} oz"
            elif '/ea' in string:
                #This is the worst outcome so we want to append it to a list for later
                possible.append(f"{self.stringValueExtraction(string, '/ea')}/ea")
        return next((item for item in possible if item is not None), None)
        
    #Heirloom tomatoes are tricky 
    def heirloomTomatoesModifications(self, byWeight, size):
        #We can extract Organic from the name
        if self.Data['Organic'] == None:
            if 'organic' in self.Data['Product Type'].lower().replace(' ', ''): # convert to lowercase and remove spaces
                self.Data['Organic'] = 'Organic'
        #This part is for Weight
        if size != None:
            self.Data['True Weight'] = size
        elif byWeight != None:
            self.Data['True Weight'] = byWeight
        elif self.Data['True Weight'] == None:
            string = self.findWeight()
            if '/lb' in string.lower().replace(' ', ''):
                self.Data['True Weight'] = string
                self.Data['Weight in lbs'] = 1.0
                return
            else:
                self.Data['True Weight'] = string
        self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])
        
    #Helper to reduce code. Splits the string and returns the float value 
    def stringValueExtraction(self, string, stringType):
        value = ''.join(filter(lambda x: x.isdigit() or x == '.', string.split(stringType)[0]))
        if(len(value) == 0):
            return None
        return float(value)

    #Eggs don't have weight so we use amount
    def eggModifications(self):
        if self.Data['True Amount'] == None:
            checkLocations = [self.Data['Product Type'], self.Data['Current Price'], self.Data['Orignal Price']]
            for string in checkLocations:
                string = string.lower().replace(' ', '') # convert to lowercase and remove spaces
                if 'dozen' in string:
                    amount = self.stringValueExtraction(string, 'dozen')
                    if amount == None:
                        self.Data['True Amount'] = f"{1} dz"
                        self.Data['Amount in dz'] = 1.0
                        return
                    self.Data['True Amount'] = f"{amount} dz"  
                    self.Data['Amount in dz'] = amount
                    return  
                if 'dz' in string:
                    amount = self.stringValueExtraction(string, 'dz')
                    self.Data['True Amount'] = f"{amount} dz"
                    self.Data['Amount in dz'] = amount
                    return 
                if 'ct' in string:
                    amount = self.stringValueExtraction(string, 'ct')
                    self.Data['True Amount'] = f"{amount} ct"  
                    self.Data['Amount in dz'] = amount / 12
                    return
        else:
            string = self.Data['True Amount'].lower().replace(' ', '')
            if 'dozen' in string:
                amount = self.stringValueExtraction(string, 'dozen')
                if amount == None:
                    self.Data['Amount in dz'] = 1.0
                    return
                self.Data['Amount in dz'] = amount
            if 'dz' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'dz')
            if 'ct' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'ct') / 12

    def determineLocality(self,):
        localBrands = None
        nonlocalBrands = None
        #For speed we use sets and turn everyting to lowercase and no spaces for accuracy
        if(self.productIndex == 0): #Bacon
            #This is for read ability 
            #['dm bacon co', 'des moines bacon co.', 'webster city', 'berkwood farms', 'berkwood farms', 'berkwood farms', 'berkwood farms', 'berkwood farms', 'de bruin ranch']
            #['niman ranch', 'jolly posh', 'nueske', 'niman ranch']
            localBrands = {'dmbaconco', 'desmoinesbaconco.', 'webstercity', 'berkwoodfarms', 'berkwoodfarms', 'berkwoodfarms', 'berkwoodfarms', 'berkwoodfarms', 'debruinranch'}
            nonlocalBrands = {'nimanranch', 'jollyposh', 'nueske', 'nimanranch'}
        elif(self.productIndex == 1): #Eggs
            localBrands = {}
            nonlocalBrands ={}
        elif(self.productIndex == 2): #Heirloom Tomatoes
            localBrands = {}
            nonlocalBrands ={}
            #Sometimes it says it the name 
            if 'local' in self.Data['Product Type'].lower().replace(' ', ''): # convert to lowercase and remove spaces
                self.Data['Local'] = 'Local'
                return
        #Add product brands here
        else:
            #Catch if no brands are set for the product
            raise BrandingError(self.productIndex)
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