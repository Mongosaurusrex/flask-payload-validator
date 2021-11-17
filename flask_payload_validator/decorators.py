from functools import wraps
from typing import Any, Callable, Dict, Iterable, List, Type

from flask import jsonify, request
from marshmallow import Schema, ValidationError

def validate_request(arg_schema: Type[Schema], on_error:Callable = None) -> Any:
    def normalize_query_param(value: Iterable) -> Any:
        return value if len(value) > 1 else value[0]

    def normalize_query(params: Any) -> Dict:
        return {
            k: normalize_query_param(v)
            for k, v in params.to_dict(flat=False).items()
        }

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            try:
                arguments = arg_schema().load(normalize_query(request.args))
            except ValidationError as error:
                if not on_error:
                    return jsonify({"status": "Error", "message": error.messages}), 400
                
                on_error(error.messages)
            kwargs["args"] = arguments
            return f(*args, **kwargs)
        return decorated_function
    return decorator