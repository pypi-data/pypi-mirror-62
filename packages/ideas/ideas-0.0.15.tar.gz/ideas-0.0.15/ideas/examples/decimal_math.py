"""decimal_math.py
------------------------

This replaces any Python identifier (token) a floating point variable
by a Decimal. It can be used either as an custom codec or import hook.

The source is assumed to be actually encoded in utf-8.
"""


from ideas import encoding, import_hook
import token_utils


def source_init():
    """Adds required import"""
    return "from decimal import Decimal\n"


def transform_source(source, **kwargs):
    """Simple transformation: replaces any single token λ by lambda.

    By defining this function, we can also make use of Ideas' console.
    """
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token.is_number() and "." in token.string:
            token.string = f"Decimal('{token.string}')"

    return token_utils.untokenize(tokens)


def register(add_init=None):
    if add_init:
        add_init = source_init

    encoding.register_encoding(
        encoding_name="decimal-math",
        transform_source=transform_source,
        source_init=add_init,
        hook_name=__name__,
    )


def add_hook(verbose_finder=False):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_source=transform_source,
        verbose_finder=verbose_finder,
    )
    return hook
