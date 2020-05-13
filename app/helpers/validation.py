from schema import Schema, And, Use


def validate(schema_name, json_data):
    if schema_name == 'predict':
        schema = _predict_schema()
    else:
        raise NotImplementedError("Schema name: '{}' not found.".format(schema_name))

    # let exceptions bubble up
    schema.validate(json_data)


def _predict_schema():
    schema = Schema(
        {
            'id': And(Use(str)),   #unique car id, (must be string)
            'manufacturer': And(Use(str)), # e.g toyota, honda, nissan, etc.. (must be string)
            'mileage': And(Use(float)), #mileage in Km (must be number; integer or float)
            'year': And(Use(int)), #year of make  (must be greater than 1980 and less than or equal to the current year (e.g 2020 as at present))
            'sec_status': And(Use(str))  #must either be one of the following: Nigerian Used, New, Foreign Used (not case sensitive) 
        })

    return schema
