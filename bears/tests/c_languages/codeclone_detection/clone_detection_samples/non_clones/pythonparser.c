// From CPython: https://hg.python.org/cpython

typedef struct _nfaarc {
    int         ar_label;
    int         ar_arrow;
} nfaarc;

typedef struct _nfastate {
    int         st_narcs;
    nfaarc      *st_arc;
} nfastate;

typedef struct _nfa {
    int                 nf_type;
    char                *nf_name;
    int                 nf_nstates;
    nfastate            *nf_state;
    int                 nf_start, nf_finish;
} nfa;

// dummy
typedef char** labellist;

typedef struct _nfagrammar {
    int                 gr_nnfas;
    nfa                 **gr_nfa;
    labellist           gr_ll;
} nfagrammar;

void Py_FatalError(char*);

void addlabel(labellist*, int, char*);
nfa* newnfa(char*);
void *PyObject_REALLOC(nfa**, int);

struct tok_state
{
    char* buf;
    char* cur;
    char* end;
    char* inp;
};

struct tok_state *tok_new();
const char* decode_str(const char *, int, struct tok_state*);
void PyTokenizer_Free(struct tok_state *);

static nfa *
addnfa(nfagrammar *gr, char *name)
{
    nfa *nf;

    nf = newnfa(name);
    gr->gr_nfa = (nfa **)PyObject_REALLOC(gr->gr_nfa,
                                  sizeof(nfa*) * (gr->gr_nnfas + 1));
    if (gr->gr_nfa == NULL)
        Py_FatalError("out of mem");
    gr->gr_nfa[gr->gr_nnfas++] = nf;
    addlabel(&gr->gr_ll, NAME, nf->nf_name);
    return nf;
}

struct tok_state *
PyTokenizer_FromString(const char *str, int exec_input)
{
    struct tok_state *tok = tok_new();
    if (tok == NULL)
        return NULL;
    str = decode_str(str, exec_input, tok);
    if (str == NULL) {
        PyTokenizer_Free(tok);
        return NULL;
    }

    /* XXX: constify members. */
    tok->buf = tok->cur = tok->end = tok->inp = (char*)str;
    return tok;
}
