ROBOT_SCHEMA = {
    "type": "object",
    "properties": {
        "model": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2,
        },
        "version": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2,
        },
        "created": {"type": "string", "format": "date-time"}
    },
    "required": ["model", "version", "created"]
}
