import pandas as pd

# This class is here to handle the branding of proucts


class BrandIdentification():
    def __init__(self):
        self.getLocalBrands = [
            #Bacon
            {'oconnellorganicacres', 'winneshiekbeefporkpoultry','hartcountrymeats','iowafoodhub', 'humblehandsharvest','hormelblacklabel', 'newpi', 'desmoinesbaconandmeatcompany', 'desmoinesbaconmeatcompany', 'desmoinesbaconco','berkwoodfarms', 'joiagoodfarm', 'beeler', 'dmbaconco', 'prairiefresh', 'webstercity', 'hyvee', 'hickorycountry'},
            #Eggs
            {'kymaracres', 'hotzeggs', 'cosgroverdfarm', 'steineckefamilyfarm', 'farmershenhouse', 'cedarridgefarm', 'joiafoodfarm', 'thatssmart', 'hyvee', 'beavercreekfarm'},
            #Heirloom Tomatoes
            {'seedsavers'},
            #All Tomatoes
            {'seedsavers', 'fullcirclemarket', 'basketbushel', 'sunnyvalley'}
        ]

        self.getNonLocalBrands = [
            #Bacon
            {'hatfield', 'mullanroad', 'jollyposh', 'farmland', 'countrysmokehouse', 'herbivorousbutcher', 'bigbuy', 'nimanranch', 'jimmydean', 'farmpromise', 'hormel', 'plainvillefarms', 'nueske', 'smithfield', 'applegate', 'garrettvalley', 'pedersonsnaturalfarms', 'indianakitchen', 'freshthyme', 'oscarmayer', 'jamestown', 'debruinranch', 'wright', 'boarshead'},
            #Eggs
            {'stateline', 'freshthyme', 'bornfree', 'handsomebrookfarm', 'handsomebrookfarms', 'egglandsbest', 'peteandgerryseggs', 'pennysmart', 'bestchoice', 'nellies', 'vitalfarms', 'organicvalley', 'happyegg'},
            #Heirloom Tomatoes
            {'organicvalley', 'delcabo'},
            #All Tomatoes
            {'organicvalley', 'delcabo', 'redsunfarms', 'wholesumharvest', 'sunset', 'naturefresh', 'wildwonders', 'naturesweet', 'angelsweet'}
        ]

        self.getBrandNames = [
            #Bacon
            {'Hatfield', "O'connell organic acres",'Winneshiek beef pork & poultry', 'Hart country meats', 'Iowa food hub', 'Humble hands harvest', 'Mullan road', 'Hormel black label', 'New pi', "Des moines bacon & meat company", 'Jimmy dean', 'Oscar mayer', 'Jolly posh','Webster city', 'Prairie fresh', 'Des-moines-bacon-and-meat-company', "Boar's head", 'Fresh thyme', 'Country-smokehouse', 'Farm promise', 'Hormel', 'Oscar-mayer', 'Smithfield', 'Farmland', 'De bruin ranch', 'Indiana kitchen', "Pederson's natural farms", 'Des moines bacon co', 'Applegate', 'Country smokehouse', 'Niman ranch', 'Jolly posh', 'Berkwood farms', 'Hyvee', 'Jimmy-dean', 'Dm bacon co', 'Herbivorous butcher', 'Hickory country', 'Hy-vee', 'Beeler', 'Joia food farm', 'Garrett valley', 'Deli', 'Jamestown', 'Plainville farms', 'Big buy', 'Nueske', 'Wright'},            
            #Eggs
            {'Kymar acres', 'Hotz eggs', 'Cosgrove rd farm', 'Steinecke family farm', "That's smart", "Egglands best", "Pete and gerry's eggs" ,"Nellie's", "Eggland's best", 'Handsome brook farm', 'Egglands-best', 'Farmers hen house', 'Handsome brook farms', 'Joia food farm', 'Penny smart', 'Fresh thyme', 'Vital farms', 'Best choice', 'Nellies-eggs', 'Organic valley', 'Cedar ridge farm', 'Happy egg', 'Thats-smart', 'Pete-and-gerrys-eggs', 'Farmers-hen-house', 'Beaver creek farm', 'Born free', 'Stateline', 'Hyvee', 'Hy-vee'},
            #Heirloom Tomatoes
            {'Del cabo', 'Seed savers', 'Organic valley'},
            #All Tomatoes
            {'Del cabo', 'Seed savers', 'Organic valley', 'Wild wonders', 'Nature sweet', 'Wholesum harvest', 'Red sun farms', 'Sunnyvalley', 'Angel sweet', 'Full circle market', 'Sunset', 'Basket & bushel', 'Nature fresh'}
        ]
        
        #If the brand is any of these we cant tell the locality
        self.getCantDeterminedBrand = {'deli'}
                
    def determineLocality(self, inputBrand, inputProduct, productIndex):
        locality = None
        brand = None         
        if pd.isnull(inputBrand):
            #Find the brand name
            if inputProduct: 
                name = ' '.join(inputProduct.split()).lower() # remove extra spaces
                name = ''.join(c for c in name if c.isalpha() or c == "'" or c == " " or c == "-" or c == "&") # keep only letters, apostrophes, hyphens, and spaces and capitalize the first letter
                name = name.capitalize()
                brand = ''
                for b in self.getBrandNames[productIndex]:
                    if b in name and len(b) > len(brand):
                        brand = b
                brand = brand.lower().capitalize()
        else:
            brand = inputBrand.lower().capitalize()
        #Converts the brand into something we can quickly compair
        if brand:
            formatBrand = ''.join(c for c in brand if c.isalpha()).lower()
            #Determins locality
            if formatBrand in self.getLocalBrands[productIndex]:
                locality = "Local"
            elif formatBrand in self.getNonLocalBrands[productIndex]:
                locality = "Non-local"
            elif formatBrand in self.getCantDeterminedBrand:
                locality = "Can't be Determined"
        if productIndex == 2 or productIndex == 3: #Special condition for Tomatoes
            #Sometimes what we need is in the name
            name = inputProduct.lower().replace(' ', '')
            if 'local' in name: # convert to lowercase and remove spaces
                locality = 'Local'
        return brand, locality
    
    #Two Helper functions in case we need to add more brands to the loadBrands function above
    #for the getBrandNames
    def CleanStringList(self, strings):
        cleaned = set()
        for s in strings:
            s = ''.join(c for c in s if c.isalpha()).lower() # keep only letters
            cleaned.add(s)
        print(list(cleaned))

    # #for the getLocalBrands and getNonLocalBrands
    def CleanStringNames(self, strings):
        cleaned = set()
        for s in strings:
            name = ' '.join(s.split()).lower() # remove extra spaces
            name = ''.join(c for c in name if c.isalpha() or c == "'" or c == " " or c == "-").capitalize() # keep only letters, apostrophes, hyphens, and spaces and capitalize the first letter
            cleaned.add(name)
        print(list(cleaned))
    