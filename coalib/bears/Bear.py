from coalib.settings.FunctionMetadata import FunctionMetadata


def copy_metadata(source, target, omit):
    if hasattr(source, "__metadata__"):
        target.__metadata__ = source.__metadata__
    else:
        target.__metadata__ = FunctionMetadata.from_function(source, omit)


def bear(func):
    def invoke_bear(**kwargs):
        func(**kwargs)

    copy_metadata(func, invoke_bear, ('self', ))
    return invoke_bear
