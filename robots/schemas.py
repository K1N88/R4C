robot_schema = {
    "type": "object",
    "properties": {
        "model": {"type": "string"},
        "version": {"type": "string"},
        "created": {"type": "string", "format": "date-time"}
    },
    "required": ["model", "version", "created"]
}
