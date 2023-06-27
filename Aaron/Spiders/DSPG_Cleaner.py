from DSPG_SpiderErrors import DataCleanerError
from DSPG_SpiderErrors import BrandingError
from DSPG_SpiderErrors import StringValueExtractionError
from datetime import datetime
import re

#This is a helper class to reduce duplicate code in the DataCleaner class
class DataCleaner():

    def __init__(self):
        self.getLocalBrands = [
            #Bacon
            {'oconnellorganicacres', 'winneshiekbeefporkpoultry','hartcountrymeats','iowafoodhub', 'humblehandsharvest','hormelblacklabel', 'newpi', 'desmoinesbaconandmeatcompany', 'desmoinesbaconmeatcompany', 'desmoinesbaconco','berkwoodfarms', 'joiagoodfarm', 'beeler', 'dmbaconco', 'prairiefresh', 'webstercity', 'hyvee', 'hickorycountry'},
            #Eggs
            {'kymaracres', 'hotzeggs', 'cosgroverdfarm', 'steineckefamilyfarm', 'farmershenhouse', 'cedarridgefarm', 'joiafoodfarm', 'thatssmart', 'hyvee', 'beavercreekfarm'},
            #Heirloom Tomatoes
            {'seedsavers'}
        ]

        self.getNonLocalBrands = [
            #Bacon
            {'mullanroad', 'jollyposh', 'farmland', 'countrysmokehouse', 'herbivorousbutcher', 'bigbuy', 'nimanranch', 'jimmydean', 'farmpromise', 'hormel', 'plainvillefarms', 'nueske', 'smithfield', 'applegate', 'garrettvalley', 'pedersonsnaturalfarms', 'indianakitchen', 'freshthyme', 'oscarmayer', 'jamestown', 'debruinranch', 'wright', 'boarshead'},
            #Eggs
            {'stateline', 'freshthyme', 'bornfree', 'handsomebrookfarm', 'handsomebrookfarms', 'egglandsbest', 'peteandgerryseggs', 'pennysmart', 'bestchoice', 'nellies', 'vitalfarms', 'organicvalley', 'happyegg'},
            #Heirloom Tomatoes
            {'organicvalley', 'delcabo'}
        ]

        self.getBrandNames = [
            #Bacon
            {"O'connell organic acres",'Winneshiek beef pork & poultry', 'Hart country meats', 'Iowa food hub', 'Humble hands harvest', 'Mullan road', 'Hormel black label', 'New pi', "Des moines bacon & meat company", 'Jimmy dean', 'Oscar mayer', 'Jolly posh','Webster city', 'Prairie fresh', 'Des-moines-bacon-and-meat-company', "Boar's head", 'Fresh thyme', 'Country-smokehouse', 'Farm promise', 'Hormel', 'Oscar-mayer', 'Smithfield', 'Farmland', 'De bruin ranch', 'Indiana kitchen', "Pederson's natural farms", 'Des moines bacon co', 'Applegate', 'Country smokehouse', 'Niman ranch', 'Jolly posh', 'Berkwood farms', 'Hyvee', 'Jimmy-dean', 'Dm bacon co', 'Herbivorous butcher', 'Hickory country', 'Hy-vee', 'Beeler', 'Joia food farm', 'Garrett valley', 'Deli', 'Jamestown', 'Plainville farms', 'Big buy', 'Nueske', 'Wright'},            
            #Eggs
            {'Kymar acres', 'Hotz eggs', 'Cosgrove rd farm', 'Steinecke family farm', "That's smart", "Egglands best", "Pete and gerry's eggs" ,"Nellie's", "Eggland's best", 'Handsome brook farm', 'Egglands-best', 'Farmers hen house', 'Handsome brook farms', 'Joia food farm', 'Penny smart', 'Fresh thyme', 'Vital farms', 'Best choice', 'Nellies-eggs', 'Organic valley', 'Cedar ridge farm', 'Happy egg', 'Thats-smart', 'Pete-and-gerrys-eggs', 'Farmers-hen-house', 'Beaver creek farm', 'Born free', 'Stateline', 'Hyvee', 'Hy-vee'},
            #Heirloom Tomatoes
            {'Del cabo', 'Seed savers', 'Organic valley'}
        ]
        
        #If the brand is any of these we cant tell the locality
        self.getCantDeterminedBrand = {'deli'}
                

    def LoadDataSet(self, inputIndex, url):
        self.productIndex = inputIndex
        if self.productIndex == 0:
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
        elif self.productIndex == 1:
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
        elif self.productIndex == 2:
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
            #On the very rare occasion the True weight doesnt help us (This does happen)
            if not self.Data['Weight in lbs']:
                self.Data['True Weight'] = self.findWeight()
                self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])

    def ozToLb(self, input):
        if input == None:
            return None
        weight = str(input).lower()
        if 'oz' in weight:
            unit = self.stringValueExtraction(weight, 'oz') 
            return (unit / 16.0) if unit else 0.0625
        elif 'lbs' in weight:
            unit = self.stringValueExtraction(weight, 'lb')
            return unit if unit else 1.0
        elif '/lb' in weight:
            return 1.0
        elif 'lb' in weight:
            unit = self.stringValueExtraction(weight, 'lb')
            return unit if unit else 1.0 
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
            unit = self.findWeightUnit(string)
            if unit == None: 
                #Failsafe
                continue
            if "/ea" in unit:
                possible.append(unit)
            else:
                return unit
        return next((item for item in possible if item is not None), None)
    
    
    def findWeightUnit(self, string):
        string = string.lower().replace(' ', '') # convert to lowercase and remove spaces
        if 'pound' in string:
            output = self.stringValueExtraction(string, 'pound')
            if output:
                return f"{output} lb"
        if 'ounce' in string:
            output = self.stringValueExtraction(string, 'ounce')
            if output:
                return f"{output} oz"      
        if 'lbs' in string:
            output = self.stringValueExtraction(string, 'lbs')
            if output:
                return f"{output} lb"  
        if '/lb' in string:
            output = self.stringValueExtraction(string, '/lb')
            if output:
                return f"{output}/lb"  
        if 'lb' in string:
            output = self.stringValueExtraction(string, 'lb')
            if output:
                return f"{output} lb"  
        if 'oz' in string:
            output = self.stringValueExtraction(string, 'oz')
            if output:
                return f"{output} oz" 
        if '/ea' in string:
            output = self.stringValueExtraction(string, '/ea')
            if output:
                return f"{output}/ea" 
        return None
   

    
    #Heirloom tomatoes are tricky 
    def heirloomTomatoesModifications(self, weight):
        #We can extract Organic from the name
        if self.Data['Organic'] == None:
            if 'organic' in self.Data['Product Type'].lower().replace(' ', ''): # convert to lowercase and remove spaces
                self.Data['Organic'] = 'Organic'
        #This part is for Weight
        if self.Data['True Weight'] != None:
            self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])
            return
        if weight == None:
            string = self.findWeight()
            if '/lb' in string.lower().replace(' ', ''):
                self.Data['True Weight'] = string
                self.Data['Weight in lbs'] = 1.0
                return
            else:
                self.Data['True Weight'] = string
        else:
            self.Data['True Weight'] = weight
        self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])
        
    #Helper to reduce code. Splits the string and returns the float value 
    def stringValueExtraction(self, string, stringType):
        if string == None or stringType == None:
            raise StringValueExtractionError (string, stringType)
        string = string.lower().replace(' ', '')
        pattern = rf"(\d+\.\d+|\d+/\d+|\d+)(?={stringType})"
        matches = re.findall(pattern, string)
        unit =  [eval(match) for match in matches]
        return next((item for item in reversed(unit) if item is not None), None)
        
    def EggFinder(self, string):
        if string == None:
            return False
        string = string.lower().replace(' ', '') # convert to lowercase and remove spaces
        if 'halfdozen' in string:
            self.Data['True Amount'] = f"{0.5} dz"  
            self.Data['Amount in dz'] = 0.5
            return True
        if 'dozen' in string:
            amount = self.stringValueExtraction(string, 'dozen')
            if amount == None:
                self.Data['True Amount'] = f"{1} dz"
                self.Data['Amount in dz'] = 1.0
                return True
            self.Data['True Amount'] = f"{amount} dz"  
            self.Data['Amount in dz'] = amount
            return True 
        if 'dz' in string:
            amount = self.stringValueExtraction(string, 'dz')
            self.Data['True Amount'] = f"{amount} dz"
            self.Data['Amount in dz'] = amount
            return True
        if 'ct' in string:
            amount = self.stringValueExtraction(string, 'ct')
            self.Data['True Amount'] = f"{amount} ct"  
            self.Data['Amount in dz'] = amount / 12
            return True
        if 'ea' in string:
            amount = self.stringValueExtraction(string, 'ea')
            self.Data['True Amount'] = f"{amount} ea"  
            self.Data['Amount in dz'] = amount / 12
            return True
        if 'pk' in string:
            amount = self.stringValueExtraction(string, 'pk')
            self.Data['True Amount'] = f"{amount} pk"  
            self.Data['Amount in dz'] = amount / 12
            return True
        if 'pack' in string:
            amount = self.stringValueExtraction(string, 'pack')
            self.Data['True Amount'] = f"{amount} pack" 
            self.Data['Amount in dz'] = amount / 12
            return True
        return False

    #Eggs don't have weight so we use amount
    def eggModifications(self):
        if self.Data['True Amount'] == None:
            checkLocations = [self.Data['Product Type'], self.Data['Current Price'], self.Data['Orignal Price']]
            for string in checkLocations:
                if(self.EggFinder(string)):
                    return
        else:
            string = self.Data['True Amount'].lower().replace(' ', '')
            if 'dozen' in string:
                amount = self.stringValueExtraction(string, 'dozen')
                if amount == None:
                    self.Data['Amount in dz'] = 1.0
                    return
                self.Data['Amount in dz'] = amount
            elif 'dz' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'dz')
            elif 'ct' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'ct') / 12
            elif 'ea' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'ea') / 12
            elif 'pk' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'pk') / 12
            elif 'pack' in string:
                self.Data['Amount in dz'] = self.stringValueExtraction(string, 'pack') / 12

    def determineLocality(self):
        try:
            if self.Data['Brand'] == None:
                #Formats the name
                name = ' '.join(self.Data['Product Type'].split()).lower() # remove extra spaces
                name = ''.join(c for c in name if c.isalpha() or c == "'" or c == " " or c == "-" or c == "&") # keep only letters, apostrophes, hyphens, and spaces and capitalize the first letter
                name = name.capitalize()
                brand = ''
                for b in self.getBrandNames[self.productIndex]:
                    if b in name and len(b) > len(brand):
                        brand = b
                self.Data['Brand'] = brand
            else:
                self.Data['Brand'] = self.Data['Brand'].lower().capitalize()
            #Converts the brand into something we can quickly compair
            brand = ''.join(c for c in self.Data['Brand'] if c.isalpha()).lower()
            #Determins locality
            if brand in self.getLocalBrands[self.productIndex]:
                self.Data['Local'] = "Local"
            elif brand in self.getNonLocalBrands[self.productIndex]:
                self.Data['Local'] = "Non-local"
            elif brand in self.getCantDeterminedBrand:
                self.Data['Local'] = "Can't be Determined"
            
            if self.productIndex == 2: #Special condition for Heirloom Tomatoes
                #Sometimes what we need is in the name
                name = self.Data['Product Type'].lower().replace(' ', '')
                if 'organic' in name:
                    self.Data['Organic'] = True  
                if 'local' in name: # convert to lowercase and remove spaces
                    self.Data['Local'] = 'Local'
        except IndexError:
            raise BrandingError(self.productIndex)



#Two Helper functions in case we need to add more brands to the loadBrands function above
#for the getBrandNames
# def CleanStringList(strings):
#     cleaned = set()
#     for s in strings:
#         s = ''.join(c for c in s if c.isalpha()).lower() # keep only letters
#         cleaned.add(s)
#     print(list(cleaned))

# #for the getLocalBrands and getNonLocalBrands
# def CleanStringNames(strings):
#     cleaned = set()
#     for s in strings:
#         name = ' '.join(s.split()).lower() # remove extra spaces
#         name = ''.join(c for c in name if c.isalpha() or c == "'" or c == " " or c == "-").capitalize() # keep only letters, apostrophes, hyphens, and spaces and capitalize the first letter
#         cleaned.add(name)
#     print(list(cleaned))
