import re
from scrapy import Item
from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags, replace_escape_chars

class BikeAccessoryItem(Item):

    def format_price(value):
        price = re.match('[1-9]+[\,\.]+[1-9]+', value)

        if price is None:
            return value
        else:
            price = price.group(0).replace(",", ".")
            return float(price)

    def organize_description(list_of_values):
        result_dict = {}
        for i in range(0, len(list_of_values), 2):
            description_title = list_of_values[i].strip()
            description = list_of_values[i+1].strip()
            result_dict[description_title] = description
        return result_dict

    def organize_store_stock_info(list_of_values):
        result_dict = {}
        for i in range(0, len(list_of_values), 4):
            store_name = list_of_values[i].strip()
            store_address = list_of_values[i+1].strip()
            store_city = list_of_values[i+2].strip()
            stock_info = list_of_values[i+3].strip()
            result_dict[store_name] = [store_address, store_city, stock_info]
        return result_dict

    product_url = Field(
        output_processor = TakeFirst()
    )

    title = Field(
        input_processor = MapCompose(remove_tags, replace_escape_chars),
        output_processor = TakeFirst()
    )
    price = Field(
        input_processor = MapCompose(remove_tags, replace_escape_chars),
        output_processor = TakeFirst(),
        serializer = format_price
    )    
    image_url = Field(
        input_processor = MapCompose(remove_tags, replace_escape_chars),
        output_processor = TakeFirst()
    )
    serial_num = Field(
        input_processor = MapCompose(remove_tags, replace_escape_chars),
        output_processor = TakeFirst()
    )
    description = Field(
        input_processor = MapCompose(remove_tags, replace_escape_chars),
        serializer = organize_description
    )
    store_stock_info = Field(
        input_processor = MapCompose(remove_tags, replace_escape_chars),
        serializer = organize_store_stock_info
    )