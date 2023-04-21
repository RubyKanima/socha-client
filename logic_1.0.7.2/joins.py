import logging

class Joins():
    '''
    the `Joins` class contains a series of function for joining two lists which are not tupels

    all basic joins compare the `items` from the left list and right list
    - Parameters:
        - `left`
        - `right`

    all on joins compare the `attributes` from each `item` from left and right
    - Parameters:
        - `left`
        - `right`
        - `attr`
        - `only_attr`:bool
    '''

    # join

    def left_outer_join(left: any, right: any) -> list:
        '''
        left_outer_join contains all items from the left list which are not in the right list

        `if left[item] != right[item]` -> `[left[item]]`
        '''
        return [each for each in left if each not in right]

    def right_outer_join(left: any, right: any) -> list:
        '''
        right_outer_join contains all items from the left list which are not in the right list

        `if right[item] != left[item]` -> `[right[item]]`
        '''
        return [each for each in right if each not in left]
    
    def inner_join(left: any, right: any) -> list:
        '''
        inner_join contains all items from the left list which are in the right list

        `if left[item] == right[item]` -> [left[item] or right[item]]
        '''
        return [each for each in left if each in right]
    
    def outer_join(left: any, right: any) -> list:
        '''
        outer_join contains all items from the left list which are not in the right list and all items from the right list which are not in the left list

        `left_outer_join + right_outer_join`
        '''
        return Joins.left_outer_join(left,right).extend(Joins.right_outer_join(left, right))
    
    # join on

    def left_outer_join_on(left: any, right: any, attr, only_attr = False) -> list:
        ''' missing code '''

    def right_outer_join_on(left: any, right: any, attr, only_attr = False) -> list:
        ''' missing code '''

    def left_join_on(left: any, right: any, attr, only_attr = False) -> list:
        ''' missing code'''    

    def right_join_on(left: any, right: any, attr, only_attr = False) -> list:
        ''' missing code'''

    def left_inner_join_on(left: any, right: any, attr, only_attr = False):
        '''
        left_inner_join returns the left values of an inner_join_on

        `if left_item[attribute] == right_item[attribute]` -> `[left_item]` or `[left_item[attribute]]`
        '''

        return [each[0] for each in Joins.inner_join_on(left, right, attr, only_attr)]
    
    def right_inner_join_on(left: any, right: any, attr, only_attr = False):
        '''
        right_inner_join_on  returns the right values of an inner_join_on

        `if left_item[attribute] == right_item[attribute]` -> `[right_item]`or `[right_item[attribute]]`
        '''

        return [each[1] for each in Joins.inner_join_on(left, right, attr, only_attr)]

    def inner_join_on(left: any, right: any, attr, only_attr = False) -> list:
        '''
        inner_join_on returns a list of all items from a left list whose item's attribute equals to the attribute of right list's item

        `if left_item[attribute] == right_item[attribute]` -> `[[left_item],[right_item]]` or `[attribute]`
        '''
        if not isinstance(left, type(right)):
            logging.error(f"TypeError: {type(left)} does not equal {type(right)}")
            raise TypeError
        try:
            if isinstance(left[0], type(right[0])):
                _type = type(left[0])
            else:
                raise TypeError
            if only_attr:
                if _type == list | dict:
                    return [each[attr] for each in left for other in right if each[attr] == other[attr]]
                return [getattr(each, attr) for each in left for other in right if getattr(each, attr) == getattr(other, attr)]
            else:
                if _type == list | dict:
                    return [[each, other] for each in left for other in right if each[attr] == other[attr]]
                return [[each, other] for each in left for other in right if getattr(each, attr) == getattr(other, attr)]
        except AttributeError:
            logging.error(f"Attribute {attr} is not in {left} or {right}")
        except ValueError:
            logging.error(f"{attr} does not fit {_type}")

    def outer_join_on(left: any, right: any , attr, only_attr = False) -> list:
        ''' missing code'''

        '''
        outer_join_on returns a list of all outer_left_join_on and outer_right_join_on items

        `outer_left_join_on + outer_right_join_on`
        '''
