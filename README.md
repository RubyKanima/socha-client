<a target="_blank" rel="noopener noreferrer" href="https://www.software-challenge.de"><p align="center"><img width="128" src="https://software-challenge.de/site/themes/freebird/img/logo.png" alt="Software-Challenge Logo"></p></a>
[![Read the Docs](https://img.shields.io/readthedocs/software-challenge-python-client?label=Docs)](https://software-challenge-python-client.readthedocs.io/en/latest/)
[![Socha](https://img.shields.io/badge/Socha-Packages-green)](https://software-challenge-python-client.readthedocs.io/en/latest/socha.html)
[![PyPI](https://img.shields.io/pypi/v/socha?label=PyPi)](https://pypi.org/project/socha/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/socha?label=Python)](https://pypi.org/project/socha/)
[![Documentation](https://img.shields.io/badge/Software--Challenge%20-Documentation-%234299e1)](https://docs.software-challenge.de/)
<h1> ペンギンの神 (Pengin no Kami)</h1>
<h3> Introduction </h3>
Each changelog should contain general changes of the bot's behaviour. Furhtermore it should also contain all files, classes, functions and variable changes.
Images can be used and should only be used as far as it contributes to the subject. Code examples aren't necessary although they can come in handy for certain runtime discussions and special functionality.

<h3> Dress-Code / Formatting </h3>

The code should be viewable wihtout any confusion which leads to following rules for formatting:
  - **Type declaration**
  
    If not clear, the declaration of variable types are needed.
    
    ```python
    i: int = None
    text: str = None
    lists: list = None
    list_in_list: list[list[]] = None
    anything: any = None
    any_class: Class = None
    ```    
        
  - **Comments**
  
    If you want to take notes on a class or function you can make use of VisualStudios comment features like the following
    
    ```python
    class Test():
      ''' This is a `Test` class '''
      def __init__(self, num: int, txt: str, yn: bool):
        '''
        This is the initialization of the `Test` class

        Parameters:
          - num: int
          - txt: str
          - yn: bool
        '''
    ```
          
    ![Example of VisualStudio,hovering over the function](https://cdn.discordapp.com/attachments/650346356111835166/1098816682765586463/image.png)
  
  - **Unnesting**
    
    Nesting is describing the excessive use of indents which can be prevented. It mostly occures in multiple if-statements or for-loops
    
    **Unnesting with return**
    
    ```python
    def return_smaller_int(first_num: int, second_num: int):
      if first_num < second_num:
        return first_num
      else:
        return second_num
    ```
   
    This Code can easily be shortened in multiple ways. The first is intermediate but quite genius; 
    The function will end as soon as a value is returned which leads to this solution:
   
    ```python
    def return_smaller_int(first_num: int, second_num: int):
      if first_num < second_num:
        return first_num
      return second_num
    ```
   
    Although it seems a little cheesy, you can completely delete this function because it already exists!
    Here you could easily use the `max()` or `min()` function. And don't worry about your performance;
    Integrated functions are most likely faster because they're written in C. There are only a few exceptions.
   
    ```python
    min(first_num, second_num)
    ```
  
    More Unnesting Tips: [Youtube: Why You Shouldn't Nest Your Code](https://www.youtube.com/watch?v=CFRhGnuXG-4)
   
  - **Consistency**
    
    Don't use different names for the same variable in different functions and make a function describe itself:
    
    ```python
    def evaluate(state: GameState):
      return len(state.possible_moves) - len(state.other_possible_moves) 

    def evaluate2(current_state: GameState):
      return len(current_state.opp_moves) - len(current_state.poss_moves)
    ```
    
    You should rather do something like this:
    
    ```python
    def delta_current_possible_moves(state: GameState):
      return len(state.possible_moves) - len(state.other_possible_moves)

    def delta_other_possible_moves(state: GameState):
      return len(state.other_possible_moves) - len(state.possible_moves)
    ```
          
