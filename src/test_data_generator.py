import unittest
from data_generator import generate_random_data

class TestGenerateRandomData(unittest.TestCase):

    def test_generate_integer(self):
        schema = {"type": "integer", "minimum": 10, "maximum": 20}
        result = generate_random_data({"properties": {"value": schema}})
        self.assertIn(result["value"], range(10, 21))

    def test_generate_string(self):
        schema = {"type": "string"}
        result = generate_random_data({"properties": {"value": schema}})
        self.assertIsInstance(result["value"], str)
        self.assertEqual(len(result["value"]), 10)

    def test_generate_boolean(self):
        schema = {"type": "boolean"}
        result = generate_random_data({"properties": {"value": schema}})
        self.assertIn(result["value"], [True, False])

    def test_generate_enum(self):
        schema = {"enum": ["red", "green", "blue"]}
        result = generate_random_data({"properties": {"value": schema}})
        self.assertIn(result["value"], ["red", "green", "blue"])

    def test_generate_array(self):
        schema = {"type": "array", "items": {"type": "integer"}}
        result = generate_random_data({"properties": {"value": schema}})
        self.assertIsInstance(result["value"], list)
        self.assertTrue(all(isinstance(x, int) for x in result["value"]))

    def test_generate_object(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        result = generate_random_data({"properties": {"value": schema}})
        self.assertIn("name", result["value"])
        self.assertIn("age", result["value"])
        self.assertIsInstance(result["value"]["name"], str)
        self.assertIsInstance(result["value"]["age"], int)

    def test_required_fields(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        result = generate_random_data(schema)
        self.assertIn("name", result)
        self.assertIn("age", result)


if __name__ == "__main__":
    unittest.main()
