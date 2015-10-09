# -*- coding: utf-8 -*-

from rdflib import Graph, URIRef, BNode
from rdflib.namespace import RDF

__all__ = ['parse']


def parse(page):
    g = Graph()
    g.parse(data=page, format="microdata")

    places = ((s, schema(o)) for s, p, o in g.triples((None, RDF.type, None))
              if is_place(o))
    return [collect(g, place, category) for place, category in places]


def collect(graph, current, category=None):
    result = {u'CATEGORY': category} if category else dict()
    for p, o in graph.predicate_objects(current):
        key = schema(p)
        if key:
            value = collect(graph, o) if isinstance(o, BNode) else pretty(o)
            current = result.get(key)
            if value is None or value == dict():
                pass
            elif current is None:
                result.update({key: value})
            elif isinstance(current, list):
                result.update({key: current + [value]})
            else:
                result.update({key: [current, value]})
    return result


def pretty(text):
    substitues = {u'\t': u' ', u'\n': u' ', u'\r': u' ', u'\v': u' '}
    translated = ''.join(substitues.get(c, c) for c in text)
    return ' '.join(a for a in translated.split(' ') if a != u'')


def schema(obj):
    split = obj.split('http://schema.org/')
    if len(split) == 2 and len(split[0]) == 0:
        return split[1]
    return None


def is_place(obj):
    return schema(obj) in CATEGORIES


CATEGORIES = {
    'LocalBusiness', 'AnimalShelter', 'AutomotiveBusiness', 'AutoBodyShop',
    'AutoDealer', 'AutoPartsStore', 'AutoRental', 'AutoRepair', 'AutoWash',
    'GasStation', 'MotorcycleDealer', 'MotorcycleRepair', 'ChildCare',
    'DryCleaningOrLaundry', 'EmergencyService', 'FireStation', 'Hospital',
    'PoliceStation', 'EmploymentAgency', 'EntertainmentBusiness',
    'AdultEntertainment', 'AmusementPark', 'ArtGallery', 'Casino',
    'ComedyClub', 'MovieTheater', 'NightClub', 'FinancialService',
    'AccountingService', 'AutomatedTeller', 'BankOrCreditUnion',
    'InsuranceAgency', 'FoodEstablishment', 'Bakery', 'BarOrPub', 'Brewery',
    'CafeOrCoffeeShop', 'FastFoodRestaurant', 'IceCreamShop', 'Restaurant',
    'Winery', 'GovernmentOffice', 'PostOffice', 'HealthAndBeautyBusiness',
    'BeautySalon', 'DaySpa', 'HairSalon', 'HealthClub', 'NailSalon',
    'TattooParlor', 'HomeAndConstructionBusiness', 'Electrician',
    'GeneralContractor', 'HVACBusiness', 'HousePainter', 'Locksmith',
    'MovingCompany', 'Plumber', 'RoofingContractor', 'InternetCafe', 'Library',
    'LodgingBusiness', 'BedAndBreakfast', 'Hostel', 'Hotel', 'Motel',
    'MedicalOrganization', 'Dentist', 'DiagnosticLab', 'Hospital',
    'MedicalClinic', 'Optician', 'Pharmacy', 'Physician', 'VeterinaryCare',
    'ProfessionalService', 'AccountingService', 'Attorney', 'Dentist',
    'Electrician', 'GeneralContractor', 'HousePainter', 'Locksmith', 'Notary',
    'Plumber', 'RoofingContractor', 'RadioStation', 'RealEstateAgent',
    'RecyclingCenter', 'SelfStorage', 'ShoppingCenter',
    'SportsActivityLocation', 'BowlingAlley', 'ExerciseGym', 'GolfCourse',
    'HealthClub', 'PublicSwimmingPool', 'SkiResort', 'SportsClub',
    'StadiumOrArena', 'TennisComplex', 'Store', 'AutoPartsStore', 'BikeStore',
    'BookStore', 'ClothingStore', 'ComputerStore', 'ConvenienceStore',
    'DepartmentStore', 'ElectronicsStore', 'Florist', 'FurnitureStore',
    'GardenStore', 'GroceryStore', 'HardwareStore', 'HobbyShop',
    'HomeGoodsStore', 'JewelryStore', 'LiquorStore', 'MensClothingStore',
    'MobilePhoneStore', 'MovieRentalStore', 'MusicStore',
    'OfficeEquipmentStore', 'OutletStore', 'PawnShop', 'PetStore', 'ShoeStore',
    'SportingGoodsStore', 'TireShop', 'ToyStore', 'WholesaleStore',
    'TelevisionStation', 'TouristInformationCenter', 'TravelAgency'
}
