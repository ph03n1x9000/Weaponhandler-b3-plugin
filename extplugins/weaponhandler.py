# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Uses the logic of AntiNoob plugin for B3

__version__ = '1.2.0'
__author__ = 'ph03n1x'

from b3.plugin import Plugin


class WeaponInfo:
    def __init__(self, weapon, mod, rule, penalty):
        self.weaponID = weapon
        self.mod = mod
        self.rule = rule
        self.penalty = penalty


# ------------------------------------------------------------------------ #
class WeaponhandlerPlugin(Plugin):
    _adminplugin = None
    weaponrestrictlist = []

    def onStartup(self):
        self.registerEvent('EVT_CLIENT_KILL', self.onkillordamage)
        self.registerEvent('EVT_CLIENT_DAMAGE', self.onkillordamage)
        self._adminplugin = self.console.getPlugin('admin')

        if not self._adminplugin:
            self.error('Could not find admin plugin')
            return

    def onLoadConfig(self):
        for entry in self.config.get('penalties/weapon'):  # Load penalties
            if entry.text:
                weapon = entry.text
            else:
                weapon = ''
            mod = entry.get('mod')
            rule = entry.get('rule')
            penalty = entry.get('penalty')
            
            if mod != '' or weapon != '':
                self.debug('Weapon penalty loaded: >' + weapon + '< Mod:>' +
                           mod + '<rule:>' + rule + '<penalty:>' + penalty + '<')
                self.weaponrestrictlist.append(WeaponInfo(weapon, mod, rule, penalty))
            else:
                self.debug('Info: Empty settings ignored')
        
    # -------------------------- EVENT HANDLING --------------------------------
    def onkillordamage(self, event):
        weapon = event.data[1]
        mod = event.data[3]
        self.handleweapon(weapon, mod, event.client)

    def handleweapon(self, weapon, mod, player):
        """
        Handle a kill or damage made with a weapon
        :param weapon: The weapon used by player
        :param mod: The weapon mod used
        :param player: The player using the weapon
        """
        for weaponInfo in self.weaponrestrictlist:
            try:
                if weaponInfo.weaponID == weapon:
                    self.verbose('weaponID matches a restriction')
                    if weaponInfo.mod == mod:
                        self.verbose('mod also matches a restriction..penalizing')
                        wrule = weaponInfo.rule
                        wpenalty = weaponInfo.penalty
                        if wpenalty == '':
                            self.verbose('No penalty defined. Warning player')
                            self._adminplugin.warnClient(player, wrule, None, False)
                        elif wpenalty == "warn":
                            self.verbose('Warning player')
                            self._adminplugin.warnClient(player, wrule, None, False)
                        elif wpenalty == "kick":
                            self.verbose('kicking player')
                            player.kick(wrule, '', None)
                        else:
                            self.debug('Error in penalty definition')
                    elif weaponInfo.mod == "":
                        self.verbose('No mod defined. Continuing')
                        wrule = weaponInfo.rule
                        wpenalty = weaponInfo.penalty
                        if wpenalty == "":
                            self.verbose('No penalty defined. Warning player')
                            self._adminplugin.warnClient(player, wrule, None, False)
                        elif wpenalty == "warn":
                            self.verbose('Warning player')
                            self._adminplugin.warnClient(player, wrule, None, False)
                        elif wpenalty == "kick":
                            self.verbose('kicking player')
                            player.kick(wrule, '', None)
                        else:
                            self.debug('Error in penalty definition')
            except Exception, e:
                self.debug('Error: %s' % e)
