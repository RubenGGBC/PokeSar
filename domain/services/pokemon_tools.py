def pokemon_pid(pkm):
    return pkm.PID

def pokemon_sid(pkm):
    return pkm.Species

def pokemon_level(pkm):
    return pkm.CurrentLevel

def pokemon_nickname(pkm):
    return pkm.Nickname

def species_name( game_strings,species_id: int) -> str:
    s = game_strings.Species[species_id]
    return str(s)

def ability_name(game_strings, ability_id: int) -> str:
    s = game_strings.Ability[ability_id]
    return str(s)

def nature_name(game_strings, nature_id: int) -> str:
    s = game_strings.Natures[nature_id]
    return str(s)

def pokemon_types(game_strings, types: tuple)->list[str]:
    if types[0] == types[1]:
        return [str(game_strings.Types[types[0]])]
    return [str(game_strings.Types[types[0]]),str(game_strings.Types[types[1]])]

def read_stats(pkm):
    m = {"hp":"Stat_HPMax","atk":"Stat_ATK","defe":"Stat_DEF","spa":"Stat_SPA","spd":"Stat_SPD","spe":"Stat_SPE"}
    return {k:int(getattr(pkm, prop, 0)) for k,prop in m.items()}

def read_moves(game_string,pkm):
    return [game_string.Move[pkm.Move1],game_string.Move[pkm.Move2],game_string.Move[pkm.Move3],game_string.Move[pkm.Move4]]

def pokemon_item(game_string,item_id):
    return game_string.Item[item_id]