"""Stream type classes for tap-squarespace."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_squarespace.client import squarespaceStream


class ProductStream(squarespaceStream):
    """Define custom stream for Squarespace products."""
    name = "products"
    path = "/products"
    records_jsonpath = "$.products.[*]"
    primary_keys = ["id"]
    replication_key = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("type", th.StringType),
        th.Property("storePageId", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("url", th.StringType),
        th.Property("urlSlug", th.StringType),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property("isVisible", th.BooleanType),
        th.Property(
            "seoOptions",
            th.ObjectType(
                th.Property("title", th.StringType),
                th.Property("description", th.StringType),
            ),
        ),
        th.Property("variantAttributes", th.ArrayType(th.StringType)),
        th.Property(
            "variants",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("sku", th.StringType),
                    th.Property(
                        "pricing",
                        th.ObjectType(
                            th.Property(
                                "basePrice",
                                th.ObjectType(
                                    th.Property("currency", th.StringType),
                                    th.Property("value", th.StringType),
                                ),
                            ),
                            th.Property(
                                "salePrice",
                                th.ObjectType(
                                    th.Property("currency", th.StringType),
                                    th.Property("value", th.StringType),
                                ),
                            ),
                            th.Property("onSale", th.BooleanType),
                        ),
                    ),
                    th.Property(
                        "stock",
                        th.ObjectType(
                            th.Property("quantity", th.IntegerType),
                            th.Property("unlimited", th.BooleanType),
                        ),
                    ),
                    th.Property(
                        "attributes",
                        th.ObjectType(
                            th.Property("Flavor", th.StringType),
                            # Add more attribute-value pairs as needed
                        ),
                    ),
                    th.Property(
                        "shippingMeasurements",
                        th.ObjectType(
                            th.Property(
                                "weight",
                                th.ObjectType(
                                    th.Property("unit", th.StringType),
                                    th.Property("value", th.NumberType),
                                ),
                            ),
                            th.Property(
                                "dimensions",
                                th.ObjectType(
                                    th.Property("unit", th.StringType),
                                    th.Property("length", th.NumberType),
                                    th.Property("width", th.NumberType),
                                    th.Property("height", th.NumberType),
                                ),
                            ),
                        ),
                    ),
                    th.Property(
                        "image",
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("title", th.StringType),
                            th.Property("url", th.StringType),
                            th.Property(
                                "originalSize",
                                th.ObjectType(
                                    th.Property("width", th.IntegerType),
                                    th.Property("height", th.IntegerType),
                                ),
                            ),
                            th.Property(
                                "availableFormats",
                                th.ArrayType(th.StringType),
                            ),
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "images",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("altText", th.StringType),
                    th.Property("url", th.StringType),
                    th.Property(
                        "originalSize",
                        th.ObjectType(
                            th.Property("width", th.IntegerType),
                            th.Property("height", th.IntegerType),
                        ),
                    ),
                ),
            ),
        ),
        th.Property("modifiedOn", th.DateTimeType),
   
    ).to_dict()


class OrdersStream(squarespaceStream):
    """Define custom stream."""
    name = "orders"
    path = "/orders"
    primary_keys = ["id"]
    records_jsonpath = "$.result.[*]"
    replication_key = "modifiedOn"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("orderNumber", th.StringType),
        th.Property("createdOn", th.DateTimeType),
        th.Property("modifiedOn", th.DateTimeType),
        th.Property("channel", th.StringType),
        th.Property("testmode", th.BooleanType),
        th.Property("customerEmail", th.StringType),
        th.Property("billingAddress", th.ObjectType(
            th.Property("firstName", th.StringType),
            th.Property("lastName", th.StringType),
            th.Property("address1", th.StringType),
            th.Property("address2", th.StringType),
            th.Property("city", th.StringType),
            th.Property("state", th.StringType),
            th.Property("countryCode", th.StringType),
            th.Property("postalCode", th.StringType),
            th.Property("phone", th.StringType),
        )),
        th.Property("shippingAddress", th.ObjectType(
            th.Property("firstName", th.StringType),
            th.Property("lastName", th.StringType),
            th.Property("address1", th.StringType),
            th.Property("address2", th.StringType),
            th.Property("city", th.StringType),
            th.Property("state", th.StringType),
            th.Property("countryCode", th.StringType),
            th.Property("postalCode", th.StringType),
            th.Property("phone", th.StringType),
        )),
        th.Property("fulfillmentStatus", th.StringType),
        th.Property("lineItems", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("variantId", th.StringType),
            th.Property("sku", th.StringType),
            th.Property("weight", th.NumberType),
            th.Property("width", th.NumberType),
            th.Property("length", th.NumberType),
            th.Property("height", th.NumberType),
            th.Property("productId", th.StringType),
            th.Property("productName", th.StringType),
            th.Property("quantity", th.IntegerType),
            th.Property("unitPricePaid", th.ObjectType(
                th.Property("value", th.StringType),
                th.Property("currency", th.StringType),
            )),
            th.Property("variantOptions", th.ArrayType(th.ObjectType(
                th.Property("optionName", th.StringType),
                th.Property("optionValue", th.StringType),
            ))),
            th.Property("customizations", th.ArrayType(th.ObjectType(
                th.Property("label", th.StringType),
                th.Property("value", th.StringType)
            ))),
            th.Property("imageUrl", th.StringType),
            th.Property("lineItemType", th.StringType)
        ))),
        th.Property("internalNotes", th.ArrayType(th.ObjectType(
            th.Property("content", th.StringType)
        ))),
        th.Property("shippingLines", th.ArrayType(th.ObjectType(
            th.Property("method", th.StringType),
            th.Property("amount", th.ObjectType(
                th.Property("value", th.StringType),
                th.Property("currency", th.StringType)
            ))
        ))),
        th.Property("discountLines", th.ArrayType(th.ObjectType(
            th.Property("description", th.StringType),
            th.Property("name", th.StringType),
            th.Property("amount", th.ObjectType(
                th.Property("value", th.StringType),
                th.Property("currency", th.StringType),
            )),
            th.Property("promoCode", th.StringType)
        ))),
        th.Property("formSubmission", th.ArrayType(th.ObjectType(
            th.Property("label", th.StringType),
            th.Property("value", th.StringType)
        ))),
        th.Property("fulfillments", th.ArrayType(
            th.ObjectType(
                th.Property("shipDate", th.DateTimeType),
                th.Property("carrierName", th.StringType),
                th.Property("service", th.StringType),
                th.Property("trackingNumber", th.StringType),
                th.Property("trackingUrl", th.StringType)
            )
        )),
        th.Property("subtotal", th.ObjectType(
            th.Property("value", th.StringType),
            th.Property("currency", th.StringType)
        )),
        th.Property("shippingTotal", th.ObjectType(
            th.Property("value", th.StringType),
            th.Property("currency", th.StringType)
        )),
        th.Property("discountTotal", th.ObjectType(
            th.Property("value", th.StringType),
            th.Property("currency", th.StringType)
        )),
        th.Property("taxTotal", th.ObjectType(
            th.Property("value", th.StringType),
            th.Property("currency", th.StringType)
        )),
        th.Property("refundedTotal", th.ObjectType(
            th.Property("value", th.StringType),
            th.Property("currency", th.StringType)
        )),
        th.Property("grandTotal", th.ObjectType(
            th.Property("value", th.StringType),
            th.Property("currency", th.StringType)
        )),
        th.Property("channelName", th.StringType),
        th.Property("externalOrderReference", th.StringType),
        th.Property("fulfilledOn", th.DateTimeType),
        th.Property("priceTaxInterpretation", th.StringType),
    ).to_dict()
