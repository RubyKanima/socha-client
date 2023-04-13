import logging

class Joins():

    def left_join(left, right) -> list:
        return [each for each in left if each not in right]

    def right_join(left, right) -> list:
        return [each for each in right if each not in left]

    def inner_join(left, right) -> list:
        return [each for each in left if each in right]
    
    def outer_join(left, right) -> list:
        return Joins.left_join(left,right).extend(Joins.right_join(left, right))
    
    def inner_join_on(left, right, attr, only_attr = False) -> list:
        if right and not left:
            return right
            #1st exception: if only right
        if not right and left:
            return left
            #2nd exception: if only left
        if not right and not left:
            return []
            #3rd exception: if none
        
        if not isinstance(left, type(right)):
            logging.error(f"TypeError: {type(left)} does not equal {type(right)}")
            raise TypeError
            #4th exception: if not the same type

        try:
            if isinstance(left[0], type(right[0])):
                _type = type(left[0]) or type(right[0]) #check type
            else:
                raise TypeError
            if only_attr:
                if _type == list | dict:
                    return [each[attr] for each in left for other in right if each[attr] == other[attr]]
                    #5th exception: if it's a list and only attribute
                return [getattr(each, attr) for each in left for other in right if getattr(each, attr) == getattr(other, attr)]
                #6th exception: if it's an object and only attribute

            else:
                if _type == list | dict:
                    return [[each, other] for each in left for other in right if each[attr] == other[attr]]
                    #8th exception: if it's a list and complete list
                return [[each, other] for each in left for other in right if getattr(each, attr) == getattr(other, attr)]
                #9thexception: if it's an object and complete object

        except AttributeError:
            logging.error(f"Attribute {attr} is not in {left} or {right}")
        except ValueError:
            logging.error(f"{attr} does not fit {_type}")