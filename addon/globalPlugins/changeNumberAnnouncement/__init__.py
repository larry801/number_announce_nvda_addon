# -*- coding: UTF-8 -*-
# Copyright (C) 2019 RLarry Wang <larry.wang.801@gmail.com>
# This file is covered by the GNU General Public License.
# See the file LICENSE for more details.
import speechDictHandler
import ui
import globalPluginHandler
from . import _config
import addonHandler

_ = lambda x: x
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        self.digitRule = speechDictHandler.SpeechDictEntry(r"(\d)(?=\d+(\D|\b))",
                                                           r"\1 ",
                                                           "numberToDigit",
                                                           caseSensitive=False,
                                                           type=speechDictHandler.ENTRY_TYPE_REGEXP)
        tempDict = speechDictHandler.dictionaries["temp"]
        _config.load()
        config_value = _config.numberConfig["number_announce"]
        if config_value == 'single_digit':
            tempDict.append(self.digitRule)
        elif config_value == 'double_digits':
            pass

    def script_ToggleNumberAnnouncementSettings(self, gesture):
        config_value = _config.numberConfig["number_announce"]
        tempDict = speechDictHandler.dictionaries["temp"]
        if config_value == 'single_digit':
            _config.numberConfig["number_announce"] = 'number'
            tempDict.remove(self.digitRule)
            ui.message(_("Speak numbers as is."))
        elif config_value == 'number':
            _config.numberConfig["number_announce"] = 'single_digit'
            tempDict.append(self.digitRule)
            ui.message(_("Speak numbers as digits."))
        _config.save()

    script_ToggleNumberAnnouncementSettings.category = _("Number announce setting")
    script_ToggleNumberAnnouncementSettings.__doc__ = _("Toggle number announcement settings")

    __gestures = {"kb:Windows+Control+B": "ToggleNumberAnnouncementSettings"}
