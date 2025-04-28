import json
from jsonschema import validate

CONFIG_SCHEMA = {
    "type": "object",
    "required": ["device", "log", "tasks"],
    "properties": {
        "device": {
            "type": "object",
            "required": ["serial", "input"],
            "properties": {
                "serial": {"type": "string"},
                "input": {
                    "type": "object",
                    "required": ["x", "y"],
                    "properties": {
                        "x": {"type": "number", "minimum": 0},
                        "y": {"type": "number", "minimum": 0}
                    }
                }
            }
        },
        "log": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {"type": "string"}
            }
        },
        "tasks": {
            "type": "object",
            "patternProperties": {
                "^.*$": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": {"type": "number"}
                    }
                }
            }
        }
    }
}

def validate_config(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    validate(instance=config, schema=CONFIG_SCHEMA)
    print("配置文件验证通过")

if __name__ == "__main__":
    validate_config("../config/config.json")