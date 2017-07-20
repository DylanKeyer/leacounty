# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class AssessorItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = Field()
    MailingAddress = Field()
    Owner = Field()
    InCareOf = Field()
    District = Field()
    PropertyCode = Field()
    PropertyUrl = Field()
    PropertyValueInfo0 = Field()
    PropertyValueInfo1 = Field()
    PropertyValueInfo2 = Field()
    PropertyValueInfo3 = Field()
    PropertyValueInfo4 = Field()
    PropertyValueInfo5 = Field()
    PropertyValueInfo6 = Field()
    PropertyValueInfo7 = Field()
    PropertyValueInfo8 = Field()
    PropertyValueInfo9 = Field()
    EstimatedTax = Field()
    TaxYear = Field()
    CentralFullValue = Field()
    FullValue = Field()
    LandFullValue = Field()
    TaxableValue = Field()
    ImprovementsFullvalue = Field()
    ExemptValue = Field()
    PersonalPropertyFullValue = Field()
    NetValue = Field()
    ManufacturedHomeFullValue = Field()
    LivestockFullValue = Field()
    BasementSqFt = Field()
    FirstFloorSqFt = Field()
    SecondFloorSqFt = Field()
    YearBuilt = Field()
    Book = Field()
    Page = Field()
    Reception = Field()
    PhysicalAddress = Field()
    Subdivision = Field()
    Bldg = Field()
    Apt = Field()
    Section = Field()
    Range = Field()
    Township = Field()
    
    
