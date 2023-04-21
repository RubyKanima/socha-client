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
        
        i: int = None
        text: str = None
        lists: list = None
        list_in_list: list[list[]] = None
        anything: any = None
        any_class: Class = None

  - **Comments**
  
    If you want to take notes on a class or function you can make use of VisualStudios comment features like the following
    
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
          
    ![Example of VisualStudio,hovering over the function](https://cdn.discordapp.com/attachments/650346356111835166/1098816682765586463/image.png)
          
        
  - **Unnesting**
    
    Nesting is describing the excessive use of indents which can be prevented. It mostly occures in multiple if-statements or for-loops
    
    **Unnesting with return**
    
        def return_smaller_int(first_num: int, second_num: int):
          if first_num < second_num:
            return first_num
          else:
            return second_num
   
    This Code can easily be shortened in multiple ways. The first is intermediate but quite genius; 
    The function will end as soon as a value is returned which leads to this solution:
   
        def return_smaller_int(first_num: int, second_num: int):
          if first_num < second_num:
            return first_num
          return second_num
   
    Although it seems a little cheesy, you can completely delete this function because it already exists!
    Here you could easily use the `max()` or `min()` function. And don't worry about your performance;
    Integrated functions are most likely faster because they're written in C. There are only a few exceptions.
   
        min(first_num, second_num)
      
    More Unnesting Tips: [Youtube: Why You Shouldn't Nest Your Code](https://www.youtube.com/watch?v=CFRhGnuXG-4)
   
  - **Consistency**
    
    Don't use different names for the same variable in different functions and make a function describe itself:
    
        def evaluate(state: GameState):
          return len(state.possible_moves) - len(state.other_possible_moves) 
          
        def evaluate2(current_state: GameState):
          return len(current_state.opp_moves) - len(current_state.poss_moves)
    
    You should rather do something like this:
    
        def delta_current_possible_moves(state: GameState):
          return len(state.possible_moves) - len(state.other_possible_moves)
        
        def delta_other_possible_moves(state: GameState):
          return len(state.other_possible_moves) - len(state.possible_moves)
          
          
<h2>New Release: 1.0.7.2 Changelog:</h2>

<details>
  <summary> Files, Classes & Functions </summary> 
  <details> 
    <summary> logic.py </summary>

  - Logic
    - __init__
    - on_update
    - calculate_move
    - max_move (not working)
    - get_possible_movements
  - Starter

</details>

  <details> 
    <summary> joins.py </summary>
    
  - Joins
    - left_outer_join
    - right_outer_join
    - inner_join
    - outer_join
    - left_outer_join_on (missing code)
    - right_outer_join_on (missing code)
    - left_join_on (missing code)
    - right_join_on (missing code)
    - left_inner_join_on
    - right_inner_join_on
    - inner_join_on
    - outer_join_on (missing code)
    
  </details> 

  <details> 
    <summary> socha_extentions.py </summary>
    
  - Alpha_Beta
    - get_alpha_beta_fish_move
    - get_alpha_beta_inters_move
    - get_alpha_beta_cut_move
    - get_most_possible_move
    - move_hash
    - evaluate_fish
    - alpha_beta_fish
    - alpha_beta_cut
    - alpha_beta_inters
    - alpha_beta (not working)
  - Intersection
    - get_delta_cut_move
    - delta_possibles
    - delta_fish_possibles
    - _get_betweens (missing code)
    - _get_after (missing code)
  - Tree
    - get_depth_move
    - _get_depth_move
    - _depth
    - _depth_moves (basically the same as _depth)
    - depth
  - Tile (missing code)
  - Blob (missing code)
  - CustomBoard (missing code)
  </details>
</details>

<details>
  <summary> Variables </summary>
  <details>
    <summary> Logic </summary
      
**corrected**
  - `self.other_possible_moves` -> doesn't throw an error if `self.current_team` or its `opponent` is None
  - `self.full_inters`, `self.left_inters`, `self.inters_to` -> don't throw errors if `self.other_possible_moves` or `self.possible_moves` are empty
  
**added**
  - `self.left_inters`
  
**renamed** (old -> new)
  - `self.inters` -> `self.full_inters`
  
  </details>
</details>



<h2>1.0.7.1 Changelog:</h2>

<details>

<summary>
Files and Classes
</summary>

- logic.py
  - Logic
  - Starter
  
- joins.py
  - Joins
    
- socha_extentions.py
  - Depth_Search
  - Alpha_Beta
  - Intersection
    
</details>

<details>
  <summary> Variables </summary>
  <details>
    <summary> Logic </summary

**removed** because of **duplicates**
  - `self.my_team` -> `self.game_state.current_team`
  - `self.op_team` -> `self.game_state.current_team.opponent`
  - `self.poss_moves` -> `self.game_state.possible_moves`

**removed**
  - `self.rand_move` (we never want random moves)

**added**
  - `self.other_poss_moves` (possible moves from the other team)
  - `self.inters_to` (`self.inters` but only with the `to_value`)

**renamed** (old -> new)
  - `self.inner_join` -> `self.inters`
  
  </details>
</details>
