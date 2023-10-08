import ast
from dataclasses import dataclass
import json
from last.types.public import UserInfo, Placeholder
import asyncio


class Client:
    @staticmethod
    async def execute(func, kwargs_json, user_info=None):
        # Parse the JSON string to a dictionary
        kwargs = json.loads(kwargs_json)

        # If the function is a string, get its name and execute the definition
        if isinstance(func, str):
            func = func.strip()
            tree = ast.parse(func)
            func_name = tree.body[0].name
            exec(func)
            func = locals()[func_name]

        # Get the placeholders from the function's default arguments
        placeholders = {
            key: value
            for key, value in zip(func.__code__.co_varnames, func.__defaults__)
            if isinstance(value, Placeholder)
        }

        # Transform the arguments using the placeholders
        transformed_kwargs = {}
        for key, value in kwargs.items():
            if key.startswith("$"):
                key = key[1:]  # Remove the dollar sign

            # If the argument is a placeholder, use its parser
            if key in placeholders:
                value = placeholders[key].parser(value)

            transformed_kwargs[key] = value

        # Execute the function with the transformed arguments
        ret = await func(**transformed_kwargs)
        return ret
