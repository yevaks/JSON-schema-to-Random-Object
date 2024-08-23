import random
import string
import re

def generate_random_data(schema):
    def generate_value(schema_definition):
        if schema_definition is None:
            return None

        if "type" in schema_definition:
            data_type = schema_definition["type"]

            if data_type == "string":
                if "pattern" in schema_definition:
                    pattern = schema_definition["pattern"]
                    return generate_string_by_pattern(pattern)
                return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            elif data_type == "integer":
                minimum = schema_definition.get("minimum", 0)
                maximum = schema_definition.get("maximum", 100)
                return random.randint(minimum, maximum)

            elif data_type == "boolean":
                return random.choice([True, False])

            elif data_type == "array":
                item_schema = schema_definition.get("items", {})
                array_length = random.randint(1, 5)
                return [generate_value(item_schema) for _ in range(array_length)]

            elif data_type == "object":
                return generate_random_data(schema_definition)

        if "enum" in schema_definition:
            return random.choice(schema_definition["enum"])

        if "anyOf" in schema_definition:
            chosen_schema = random.choice(schema_definition["anyOf"])
            return generate_value(chosen_schema)

        return None

    def generate_string_by_pattern(pattern):
        match = re.match(pattern, "https://example.com/api/1/json/public/123/abcABC")
        if match:
            return match.group()
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    generated_data = {}
    if "properties" in schema:
        for prop, prop_schema in schema["properties"].items():
            if "default" in prop_schema:
                generated_data[prop] = prop_schema["default"]
            else:
                generated_data[prop] = generate_value(prop_schema)

    return generated_data

schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "attendees": {
      "type": "object",
      "$id": "#attendees",
      "properties": {
        "userId": {
          "type": "integer"
        },
        "access": {
          "enum": [
            "view",
            "modify",
            "sign",
            "execute"
          ]
        },
        "formAccess": {
          "enum": [
            "view",
            "execute",
            "execute_view"
          ]
        }
      },
      "required": [
        "userId",
        "access"
      ]
    }
  },
  "type": "object",
  "properties": {
    "id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "integer"
        }
      ]
    },
    "title": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "startDate": {
      "type": "integer"
    },
    "endDate": {
      "type": "integer"
    },
    "attendees": {
      "type": "array",
      "items": {
        "$ref": "#attendees"
      },
      "default": []
    },
    "parentId": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "string"
        },
        {
          "type": "integer"
        }
      ]
    },
    "locationId": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "integer"
        }
      ]
    },
    "process": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "string",
          "pattern": "https:\\/\\/[a-z]+\\.corezoid\\.com\\/api\\/1\\/json\\/public\\/[0-9]+\\/[0-9a-zA-Z]+"
        }
      ]
    },
    "readOnly": {
      "type": "boolean"
    },
    "priorProbability": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "integer",
          "minimum": 0,
          "maximum": 100
        }
      ]
    },
    "channelId": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "integer"
        }
      ]
    },
    "externalId": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "string"
        }
      ]
    },
    "tags": {
      "type": "array"
    },
    "form": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "viewModel": {
          "type": "object"
        }
      },
      "required": [
        "id"
      ]
    },
    "formValue": {
      "type": "object"
    }
  },
  "required": [
    "id",
    "title",
    "description",
    "startDate",
    "endDate",
    "attendees"
  ]
}

generated_data = generate_random_data(schema)
print(generated_data)
