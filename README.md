<a target="_blank" rel="noopener noreferrer" href="https://www.software-challenge.de"><p align="center"><img width="128" src="https://software-challenge.de/site/themes/freebird/img/logo.png" alt="Software-Challenge Logo"></p></a>

[![Read the Docs](https://img.shields.io/readthedocs/software-challenge-python-client?label=Docs)](https://software-challenge-python-client.readthedocs.io/en/latest/)
[![Socha](https://img.shields.io/badge/Socha-Packages-green)](https://software-challenge-python-client.readthedocs.io/en/latest/socha.html)
[![PyPI](https://img.shields.io/pypi/v/socha?label=PyPi)](https://pypi.org/project/socha/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/socha?label=Python)](https://pypi.org/project/socha/)
[![Documentation](https://img.shields.io/badge/Software--Challenge%20-Documentation-%234299e1)](https://docs.software-challenge.de/)

<h2> ペンギンの神 (Pengin no Kami) <sub>Changelog of all the different clients</sub> </h2>


<h3> New Release: 1.0.7.1 Changelog</h3>

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

<summary>
Variables
</summary>

- `self` variables from `Logic` **removed** because they are **duplicates**
  - `self.my_team` -> `self.game_state.current_team`
  - `self.op_team` -> `self.game_state.current_team.opponent`
  - `self.poss_moves` -> `self.game_state.possible_moves`

- `self` variables from `Logic` **removed**
  - `self.rand_move` (we never want random moves)

- `self` variables added to `Logic`
  - `self.other_poss_moves` (possible moves from the other team)
  - `self.inters_to` (`self.inters` but only with the `to_value`)

- renamed variables in `Logic` (old -> new)
  - `self.inner_join` -> `self.inters`
