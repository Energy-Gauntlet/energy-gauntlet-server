from command import Command

def factory(cmd_type, params = {}):
  def __init__(self, new_params = {}):
    params.update(new_params)
    Command.__init__(self, cmd_type, params)
  newclass = type(cmd_type, (Command,),{"__init__": __init__})
  return newclass

Drive         = factory('drive',         { 'forwardBack': 0, 'leftRight': 0 })
VariableDrive = factory('variableDrive', { 'forwardBack': 0, 'leftRight': 0 })

TurnByDegrees = factory('furnByDegrees', { 'theDegrees': 0 })

PoleUp        = factory('poleUp')
PoleDown      = factory('poleDown')
PoleStop      = factory('poleStop')

DeployKickstands  = factory('deployKickstands')
RetractKickstands = factory('retractKickstands')
