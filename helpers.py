def set_class_property(instance, propertyName, valuesDict, required):
    if required and not contains_Key(valuesDict, propertyName):
        raise AttributeError("Required property {propertyName} not present in dictionary.")
    else:
        return setattr(instance, propertyName, valuesDict[propertyName])

def contains_Key(dict, key): 
    return key in dict.keys()