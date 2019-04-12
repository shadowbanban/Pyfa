import wx
from logbook import Logger

import eos.db
from gui.fitCommands.helpers import CargoInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class FitRemoveCargoCommand(wx.Command):

    def __init__(self, fitID, cargoInfo):
        wx.Command.__init__(self, True, 'Remove Cargo')
        self.fitID = fitID
        self.cargoInfo = cargoInfo
        self.savedRemovedAmount = None

    def Do(self):
        pyfalog.debug('Doing removal of cargo {} to fit {}'.format(self.cargoInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cargo = next((x for x in fit.cargo if x.itemID == self.cargoInfo.itemID), None)
        if cargo is None:
            return False
        self.savedRemovedAmount = min(cargo.amount, self.cargoInfo.amount)
        cargo.amount -= self.savedRemovedAmount
        if cargo.amount <= 0:
            fit.cargo.remove(cargo)
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of cargo {} to fit {}'.format(self.cargoInfo, self.fitID))
        from gui.fitCommands.calc.fitAddCargo import FitAddCargoCommand
        cmd = FitAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.cargoInfo.itemID, amount=self.savedRemovedAmount))
        return cmd.Do()
