from coalib.bearlib.languages.Language import Language


@Language
class CUDA:
    extensions = '.cu', '.cuh'
