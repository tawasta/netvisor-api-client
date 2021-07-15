"""
    netvisor.schemas.customers.create
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013-2016 by Fast Monkeys Oy | 2019- by Heltti Oy
    :license: MIT, see LICENSE for more details.
"""
from marshmallow import fields, post_dump

from ..common import RejectUnknownFieldsSchema
from ..fields import Boolean, Decimal


class UnitPriceSchema(RejectUnknownFieldsSchema):
    amount = Decimal()
    type = fields.String()

    @post_dump
    def post_dump(self, data):
        return {
            '#text': data['amount'],
            '@type': data['type']
        }


class ProductBaseInformationSchema(RejectUnknownFieldsSchema):
    product_code = fields.String()
    product_group = fields.String()
    name = fields.String()
    description = fields.String()
    unit_price = fields.Nested(UnitPriceSchema, attribute='unit_price')
    unit = fields.String()
    unit_weight = Decimal()
    purchase_price = Decimal()
    tariff_heading = fields.String()
    comission_percentage = Decimal()
    is_active = Boolean(true='1', false='0')
    is_sales_product = Boolean(true='1', false='0')
    inventory_enabled = Boolean(true='1', false='0')
    country_of_origin = fields.String()

    class Meta:
        ordered = True


class ProductBookkeepingDetailsSchema(RejectUnknownFieldsSchema):
    default_vat_percentage = Decimal()
    default_domestic_account_number = Decimal()
    default_eu_account_number = Decimal()
    default_outside_eu_account_number = Decimal()

    class Meta:
        ordered = True


class ProductMeasureSchema(RejectUnknownFieldsSchema):
    amount = Decimal()
    unit = fields.String(default='cm')

    @post_dump
    def post_dump(self, data):
        return {
            '#text': data['amount'],
            '@unit': data['unit']
        }


class ProductPackageInformationSchema(RejectUnknownFieldsSchema):
    package_width = fields.Nested(ProductMeasureSchema)
    package_height = fields.Nested(ProductMeasureSchema)
    package_length = fields.Nested(ProductMeasureSchema)

    class Meta:
        ordered = True


class ProductWeightSchema(RejectUnknownFieldsSchema):
    amount = Decimal()
    weightunit = fields.String(default='kg')

    @post_dump
    def post_dump(self, data):
        return {
            '#text': data['amount'],
            '@weightunit': data['weightunit']
        }


class ProductAdditionalInformationSchema(RejectUnknownFieldsSchema):
    product_net_weight = fields.Nested(ProductWeightSchema)
    product_gross_weight = fields.Nested(ProductWeightSchema)
    product_package_information = fields.Nested(ProductPackageInformationSchema)

    class Meta:
        ordered = True


class DimensionSchema(RejectUnknownFieldsSchema):
    dimension_name = fields.String()
    dimension_item = fields.String()

    class Meta:
        ordered = True


class CreateProductSchema(RejectUnknownFieldsSchema):
    product_base_information = fields.Nested(ProductBaseInformationSchema)
    product_bookkeeping_details = fields.Nested(ProductBookkeepingDetailsSchema)
    product_additional_information = fields.Nested(ProductAdditionalInformationSchema)
    dimension = fields.Nested(DimensionSchema)

    class Meta:
        ordered = True

    @post_dump
    def post_dump(self, data):
        if 'country_of_origin' in data:
            data['country_of_origin'] = {
                '#text': data['country_of_origin'],
                '@type': 'ISO-3166',
            }
