import inspect, logging
from typing import Any, ClassVar, Literal, get_origin, get_args
from pydantic import BaseModel


class SignatureManager(BaseModel):
    signature: inspect.Signature
    config_included: bool

    CONFIGURATION_ARGNAME: ClassVar[Literal["config"]] = "config"

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def analyze(cls, func, *args, **kwargs):
        sig = inspect.signature(func)
        config_included = (
            True if SignatureManager.CONFIGURATION_ARGNAME in sig.parameters else False
        )
        bound_args = sig.bind(*([{}, *args] if config_included else args), **kwargs)
        bound_args.apply_defaults()

        for arg_name, arg_val in bound_args.arguments.items():
            if arg_name == SignatureManager.CONFIGURATION_ARGNAME:
                continue
            param_annotation = sig.parameters[arg_name].annotation
            if param_annotation is not inspect._empty:
                origin = get_origin(param_annotation)
                args = get_args(param_annotation)

                if origin is not None:
                    if not isinstance(arg_val, origin):
                        raise TypeError(
                            f"Arg '{arg_name}' type invalid, {param_annotation} expected, received {type(arg_val)}."
                        )
                    if args:
                        for item in arg_val:
                            if not isinstance(
                                item, args[0]
                            ):  # Simplified check for first argument
                                raise TypeError(
                                    f"Element Type Mismatch in arg '{arg_name}', received {type(item)}, expected {args[0]}"
                                )
                else:
                    if not isinstance(arg_val, param_annotation):
                        raise TypeError(
                            f"Arg '{arg_name}' type invalid, {param_annotation} expected, received {type(arg_val)}."
                        )
        return cls(signature=sig, config_included=config_included)

    def check_return(self, result: Any):
        return_annotation = self.signature.return_annotation

        if return_annotation is not inspect._empty:
            origin = get_origin(return_annotation)
            args = get_args(return_annotation)

            if origin is not None:
                if not isinstance(result, origin):
                    raise TypeError(
                        f"Return Type Mismatch, received {type(result)}, expected {return_annotation}"
                    )
                if args:
                    for item in result:
                        if not isinstance(
                            item, args[0]
                        ):  # Simplified check for first argument
                            raise TypeError(
                                f"Element Type Mismatch in return, received {type(item)}, expected {args[0]}"
                            )
            else:
                if not isinstance(result, return_annotation):
                    raise TypeError(
                        f"Return Type Mismatch, received {type(result)}, expected {return_annotation}"
                    )


class ConfigurationManager(BaseModel):
    logger: logging.Logger

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def build_config(cls, logger):
        return cls(logger=logger)
