import inspect

class ParameterManagement:
    _default_parameters = None
    _types = {"int": int, "str": str, "float": float, "dict": dict, "list": list, "set": set,
              "tuple": tuple, "None": None, "bool": bool}

    def __init__(self, function):
        self._default_parameters = self.get_parameter_function(function)

    def __get_parameter_correct_type(self, param_key, param_value):
        type_param = type(param_value)
        real_type = type(self._default_parameters[param_key])
        if type_param == real_type or real_type is None or real_type is type:
            return param_value
        try:
            type_to_cast = self._types[type_param.__name__]
            param_value = type_to_cast(param_value)
        except Exception as e:
            raise Exception("Error, type for " + str(param_key) + " is not correct")

        return param_value

    def check_hyperparameter_type(self, user_parameters: dict) -> dict:
        for param_key in user_parameters.keys():
            if param_key not in self._default_parameters.keys():
                continue
            param = self.__get_parameter_correct_type(param_key, user_parameters[param_key])
            user_parameters[param_key] = param

        return user_parameters

    @staticmethod
    def get_parameter_function(function) -> dict:

        if hasattr(function, '__call__'):
            function_signature = inspect.signature(function)
            parameters = function_signature.parameters

            args = {name: parameter.default for name, parameter in parameters.items()
                    if name not in ["self", "kwargs", "args"]}
            return args
        else:
            return {}

    def complete_parameters(self, user_parameters: dict) -> dict:
        non_defined_args = list(set(self._default_parameters.keys() - user_parameters.keys()))
        defined_args = set(self._default_parameters.keys() - non_defined_args)

        for args in defined_args:
            self._default_parameters[args] = user_parameters[args]

        return self._default_parameters
    

class SupervisedInputDataError(ValueError):
    def __init__(self, mensaje="En algoritmos supervisados es necesario proporcionar los datos de entrada y las etiquetas a predecir"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
