redirectURLEncodedJSON = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    },
    "site_transaction_id": {
      "type": "string"
    },
    "payment_method_id": {
      "type": "integer"
    },
    "card_brand": {
      "type": "string"
    },
    "bin": {
      "type": "string"
    },
    "amount": {
      "type": "integer"
    },
    "currency": {
      "type": "string"
    },
    "installments": {
      "type": "integer"
    },
    "payment_type": {
      "type": "string"
    },
    "sub_payments": {
      "type": "array",
      "items": {}
    },
    "status": {
      "type": "string"
    },
    "status_details": {
      "type": "object",
      "properties": {
        "ticket": {
          "type": "string"
        },
        "card_authorization_code": {
          "type": "string"
        },
        "address_validation_code": {
          "type": "string"
        },
        "error": {
          "type": ["string","null"]
        }
      },
      "required": [
        "ticket",
        "card_authorization_code",
        "address_validation_code",
        "error"
      ]
    },
    "date": {
      "type": "string"
    },
    "site_id": {
      "type": "string"
    },
    "pan": {
      "type": "string"
    }
  },
  "required": [
    "id",
    "site_transaction_id",
    "payment_method_id",
    "card_brand",
    "bin",
    "amount",
    "currency",
    "installments",
    "payment_type",
    "sub_payments",
    "status",
    "status_details",
    "date",
    "site_id",
    "pan"
  ]
}