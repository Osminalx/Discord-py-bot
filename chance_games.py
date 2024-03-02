from random import randint,choice


def flip_a_coin() -> int:
    selection = randint(0,1)
    return selection

def rock_paper_scissors(option) -> str:
    posible = ["Piedra","Papel","Tijeras"]
    if option in posible:
        return posible
    else:
        return "No es opción"
    
