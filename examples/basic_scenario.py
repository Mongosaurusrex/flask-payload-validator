from typing import Any, Dict
from flask import Flask
from marshmallow import Schema, fields, validate

from flask_payload_validator.decorators import validate_request

app = Flask(__name__)


class ValidationSchema(Schema):
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    order = fields.String(missing="desc", validate=validate.OneOf(["asc", "desc"]))


@app.route("/")
@validate_request(ValidationSchema)
def entry_point(args: Dict[str, Any]):
    return "All good"


if __name__ == "__main__":
    app.run(debug=True)
