from coalib.bearlib.aspects import Root


@Root.subaspect
class Security:
    """
    This aspects checks for code with flaws (or security weaknesses) in your
    codebase.
    """
    class docs:
        example = """
        char buf[1024];
        ssizet_t len;
        if ((len = readlink("/modules/pass1", buf, sizeof(buf)-1)) != -1)
            buf[len] = '\0';
        """
        example_language = 'C'
        importance_reason = """
        Security weaknesses can enable malicious users to bypass access controls
        in order to obtain unauthorized privileges, which may result in:
            * Data loss or corruption
            * Denial of access
            * Complete host system takeover
        """
        fix_suggestions = """
        Some few ways to reduce the chance of a vulnerability being used
        against a system are: the use methods that check on availability of
        memory prior to writing, the eradication of null field access and null
        method call, the eradication of redundant condition (condition whose
        result depends on which part is executed first) etc...
        """
