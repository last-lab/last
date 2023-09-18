import ast
import inspect
import json
from dataclasses import dataclass


@dataclass
class Placeholder:
    parser: callable


class Client:
    def execute(self, func, kwargs_json):
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
        return func(**transformed_kwargs)


@dataclass
class Circle:
    radius: float

    def area(self):
        return 3.14 * self.radius**2


if __name__ == "__main__":
    foo_str = """
    def foo(a=Placeholder(parser=lambda radius: Circle(radius)),
            b=Placeholder(parser=lambda b: [Circle(i) for i in b])):
        return [Circle(a.radius + i.radius).area() for i in b]
    """

    kwargs_json = json.dumps({"$a": 1, "$b": [2, 3, 4]})
    client = Client()
    print(client.execute(foo_str, kwargs_json))  # Output: [9.42, 12.56, 15.7]

    def foo(
        a=Placeholder(parser=lambda radius: Circle(radius)),
        b=Placeholder(parser=lambda b: [Circle(i) for i in b]),
    ):
        return [Circle(a.radius + i.radius).area() for i in b]

    inspect.getsource(foo)
    print(client.execute(foo, kwargs_json))  # Output: [9.42, 12.56, 15.7]
