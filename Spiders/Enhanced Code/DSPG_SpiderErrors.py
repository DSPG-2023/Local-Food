
# These are all Errors to protect you from wasting time in trying to figure out whats wrong
# It is imperative that these classes is expanded upon and used in future development  

class ProductsError(Exception):
    def __init__(self):
        self.message = "The number of Data frame added and number of products added do not match. \n Please check this in the Products class (DSPG_Products)"

class DataCleanerError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = f"Data frame not found for input index ({index}) in (DSPG_Cleaner -> Class(DataCleaner) -> function(LoadDataSet)). \n Either the input was out of range or the Data cleaning process for the product wasn't implemented just yet."

class BrandingError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = f"No brands set for product index ({index}) in DataCleaner class (DSPG_Cleaner -> Class(DataCleaner) -> function(determineLocality)). \n Brands probably wasnt set for the product just yet."

class DataFormatingError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = f"Data frame not found for input index ({index}) in (Current Spider -> Class(DataFormater) -> function(cleanUp)). \n Either the input was out of range or the Data cleaning process for the product wasn't implemented just yet."
