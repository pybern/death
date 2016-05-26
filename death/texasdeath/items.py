from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Join
 

class DeathItem(Item):
    firstName = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    lastName = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Age = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Date = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Race = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    County = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Message = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Description = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Mid = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    Education = Field(
        input_processor=MapCompose(
            unicode.strip),
        output_processor=Join())
    OILink = Field(
        input_processor=MapCompose(unicode,
            unicode.strip),
        output_processor=Join())
    OLastStatement = Field(
        input_processor=MapCompose(unicode,
            unicode.strip),
        output_processor=Join())
