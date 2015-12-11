// From GNOME Builder: https://git.gnome.org/browse/gnome-builder

typedef struct
{
    char* name;
    char* value;
} editorconfig_name_value;

typedef int special_property_name_value_pointers; // dummy

typedef struct
{
    editorconfig_name_value*                name_values;
    int                                     current_value_count;
    int                                     max_value_count;
    special_property_name_value_pointers    spnvp;
} array_editorconfig_name_value;

void free(void *);
static void set_special_property_name_value_pointers(
        const editorconfig_name_value*,
        special_property_name_value_pointers*);

static void reset_special_property_name_value_pointers(
        array_editorconfig_name_value* aenv)
{
    int         i;

    for (i = 0; i < aenv->current_value_count; ++ i)
        set_special_property_name_value_pointers(
                &aenv->name_values[i], &aenv->spnvp);
}

static void array_editorconfig_name_value_clear(
        array_editorconfig_name_value* aenv)
{
    int             i;

    for (i = 0; i < aenv->current_value_count; ++i) {
        free(aenv->name_values[i].name);
        free(aenv->name_values[i].value);
    }

    free(aenv->name_values);
}
