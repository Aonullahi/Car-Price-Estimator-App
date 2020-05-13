import numpy as np
import datetime

#Find the keys in the dictionary
def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value
        else:
            return 5

def make_feature_vector(attribute_dict):

    attribute_dict['manuyear'] = attribute_dict['manufacturer'].lower() + str(attribute_dict['year'])
    attribute_dict["status_rank"] = get_value(attribute_dict['sec_status'].lower(), status_dict)
    attribute_dict["rank"] = get_value(attribute_dict['manuyear'], model_dict)

    if ((attribute_dict["year"] > 1980)&(attribute_dict["year"] <= int(datetime.datetime.now().strftime("%Y")))):

         feature_vector = np.array([
         attribute_dict["year"],
         attribute_dict["mileage"],
         attribute_dict["status_rank"],
         attribute_dict["rank"]
         ])

        # return a row vector
         return feature_vector.reshape(1, -1)

    else:
         raise NotImplementedError("'{}' must be greater than 1980 and less than '{}'' ".format(attribute_dict["year"], int(datetime.datetime.now().strftime("%Y"))))





model_dict = {'acura1999': 2.0,
         'acura2000': 2.0,
         'acura2001': 2.5,
         'acura2002': 1.0,
         'acura2003': 3.0,
         'acura2004': 2.0,
         'acura2005': 5.0,
         'acura2006': 7.0,
         'acura2007': 6.5,
         'acura2009': 9.0,
         'acura2010': 13.0,
         'acura2013': 19.0,
         'acura2014': 16.0,
         'audi1997': 2.0,
         'bmw2004': 3.0,
         'bmw2005': 6.0,
         'bmw2006': 6.5,
         'bmw2009': 10.0,
         'bmw2015': 52.0,
         'bmw2017': 95.0,
         'cadillac2004': 10.0,
         'camry1995': 1.0,
         'camry2003': 3.0,
         'camry2007': 3.0,
         'chevrolet2005': 12.0,
         'chrysler1997': 1.0,
         'chrysler1999': 2.0,
         'chrysler2009': 4.0,
         'dodge2000': 3.0,
         'dodge2002': 2.0,
         'dodge2007': 3.5,
         'dodge2010': 3.0,
         'ford1998': 1.0,
         'ford2001': 2.0,
         'ford2002': 7.0,
         'ford2003': 3.0,
         'ford2004': 3.0,
         'ford2005': 3.0,
         'ford2006': 4.0,
         'ford2007': 5.0,
         'ford2008': 6.0,
         'ford2009': 5.5,
         'ford2010': 3.0,
         'ford2011': 7.0,
         'ford2012': 8.0,
         'ford2013': 15.0,
         'ford2014': 19.0,
         'gac2017': 12.0,
         'great2012': 2.0,
         'hiace2013': 5.0,
         'hiace2019': 100.0,
         'honda1994': 1.0,
         'honda1997': 1.0,
         'honda1998': 1.0,
         'honda1999': 1.0,
         'honda2000': 1.5,
         'honda2001': 2.5,
         'honda2002': 2.0,
         'honda2003': 2.0,
         'honda2004': 3.0,
         'honda2005': 3.0,
         'honda2006': 5.0,
         'honda2007': 4.5,
         'honda2008': 4.0,
         'honda2009': 5.5,
         'honda2010': 7.0,
         'honda2011': 8.0,
         'honda2012': 5.0,
         'honda2013': 11.0,
         'honda2014': 14.0,
         'honda2015': 19.0,
         'honda2017': 20.0,
         'hyundai1995': 1.0,
         'hyundai2001': 2.0,
         'hyundai2004': 2.0,
         'hyundai2005': 2.0,
         'hyundai2006': 2.5,
         'hyundai2007': 2.0,
         'hyundai2008': 5.0,
         'hyundai2009': 3.0,
         'hyundai2010': 3.0,
         'hyundai2011': 6.0,
         'hyundai2012': 8.5,
         'hyundai2013': 8.0,
         'hyundai2016': 18.0,
         'infiniti2002': 1.0,
         'infiniti2003': 2.0,
         'infiniti2004': 8.0,
         'infiniti2006': 3.0,
         'infiniti2007': 3.5,
         'infiniti2008': 6.5,
         'infiniti2009': 12.0,
         'infiniti2012': 10.0,
         'isuzu1999': 1.0,
         'jaguar2001': 1.0,
         'jaguar2002': 6.0,
         'jaguar2007': 12.0,
         'jaguar2013': 18.0,
         'jeep2002': 1.0,
         'jeep2003': 2.0,
         'jeep2010': 8.0,
         'kia2001': 1.0,
         'kia2003': 2.0,
         'kia2004': 2.0,
         'kia2005': 6.0,
         'kia2006': 2.0,
         'kia2007': 2.0,
         'kia2008': 2.5,
         'kia2009': 3.0,
         'kia2010': 7.0,
         'kia2011': 4.0,
         'kia2012': 7.5,
         'kia2013': 2.5,
         'kia2014': 6.5,
         'kia2015': 6.0,
         'land2001': 1.0,
         'land2006': 8.5,
         'land2007': 8.5,
         'land2008': 15.0,
         'land2009': 12.0,
         'land2010': 15.0,
         'land2011': 16.0,
         'land2012': 23.5,
         'land2014': 57.0,
         'lexus1999': 4.0,
         'lexus2000': 3.5,
         'lexus2001': 4.0,
         'lexus2002': 5.0,
         'lexus2003': 8.0,
         'lexus2004': 6.0,
         'lexus2005': 7.5,
         'lexus2006': 8.0,
         'lexus2007': 10.0,
         'lexus2008': 10.0,
         'lexus2009': 7.0,
         'lexus2013': 23.0,
         'mazda1992': 1.0,
         'mazda1998': 1.0,
         'mazda1999': 1.5,
         'mazda2000': 2.0,
         'mazda2001': 3.0,
         'mazda2002': 1.0,
         'mazda2005': 6.0,
         'mazda2006': 5.0,
         'mazda2007': 10.0,
         'mazda2009': 13.0,
         'mazda2011': 16.0,
         'mercedes-benz1996': 4.0,
         'mercedes-benz1998': 3.0,
         'mercedes-benz1999': 3.0,
         'mercedes-benz2000': 2.0,
         'mercedes-benz2002': 2.0,
         'mercedes-benz2003': 4.5,
         'mercedes-benz2004': 4.0,
         'mercedes-benz2005': 5.0,
         'mercedes-benz2006': 10.0,
         'mercedes-benz2007': 8.0,
         'mercedes-benz2008': 8.0,
         'mercedes-benz2009': 8.0,
         'mercedes-benz2010': 12.0,
         'mercedes-benz2011': 13.0,
         'mercedes-benz2012': 26.5,
         'mercedes-benz2013': 29.0,
         'mercedes-benz2014': 37.0,
         'mercedes-benz2015': 30.5,
         'mercedes-benz2016': 50.0,
         'mitsubishi1998': 3.0,
         'mitsubishi2000': 3.0,
         'mitsubishi2004': 3.0,
         'mitsubishi2008': 7.0,
         'nissan1994': 2.0,
         'nissan1995': 1.0,
         'nissan1997': 1.0,
         'nissan1999': 2.0,
         'nissan2000': 2.0,
         'nissan2001': 2.0,
         'nissan2002': 2.0,
         'nissan2003': 2.0,
         'nissan2004': 2.0,
         'nissan2005': 4.0,
         'nissan2006': 4.5,
         'nissan2007': 4.0,
         'nissan2008': 4.0,
         'nissan2009': 5.0,
         'nissan2011': 7.0,
         'nissan2012': 6.0,
         'nissan2013': 8.0,
         'opel1996': 2.0,
         'opel1997': 1.0,
         'peugeot2000': 3.0,
         'peugeot2001': 2.0,
         'peugeot2002': 2.0,
         'peugeot2003': 4.0,
         'peugeot2004': 2.5,
         'peugeot2005': 2.5,
         'peugeot2006': 5.0,
         'peugeot2008': 3.0,
         'pontiac2000': 1.0,
         'pontiac2004': 5.0,
         'pontiac2006': 3.0,
         'renault2005': 3.0,
         'saturn2007': 7.0,
         'suzuki2007': 2.0,
         'suzuki2019': 32.0,
         'toyota1992': 1.0,
         'toyota1994': 2.0,
         'toyota1996': 2.0,
         'toyota1997': 1.5,
         'toyota1998': 2.0,
         'toyota1999': 2.0,
         'toyota2000': 2.5,
         'toyota2001': 3.0,
         'toyota2002': 3.0,
         'toyota2003': 4.0,
         'toyota2004': 5.0,
         'toyota2005': 6.0,
         'toyota2006': 5.0,
         'toyota2007': 6.0,
         'toyota2008': 6.0,
         'toyota2009': 7.5,
         'toyota2010': 8.0,
         'toyota2011': 12.0,
         'toyota2012': 11.5,
         'toyota2013': 19.0,
         'toyota2014': 12.0,
         'toyota2015': 18.0,
         'toyota2016': 18.0,
         'toyota2017': 24.0,
         'toyota2018': 42.0,
         'toyota2019': 34.0,
         'volkswagen1997': 6.0,
         'volkswagen1998': 2.0,
         'volkswagen1999': 2.0,
         'volkswagen2001': 1.0,
         'volkswagen2003': 4.0,
         'volkswagen2004': 3.5,
         'volkswagen2007': 1.5,
         'volkswagen2008': 2.0,
         'volkswagen2009': 7.0,
         'volkswagen2012': 11.0,
         'volkswagen2013': 16.0,
         'volkswagen2014': 4.0,
         'volvo1998': 2.0,
         'volvo1999': 2.0,
         'volvo2004': 3.5,
         'volvo2005': 5.0,
         'volvo2006': 8.0}

status_dict = {
                "nigerian used" : 1,
                "foreign used" : 2,
                "new" : 3
               }
