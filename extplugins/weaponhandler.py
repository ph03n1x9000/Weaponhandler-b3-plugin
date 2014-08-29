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
# August 29, 2014 - v1.0.0 - Initial release


__version__ = '1.0.0'
__author__  = 'ph03n1x'

from b3 import clients
import b3, string, re, threading
import b3.events
import b3.plugin


class WeaponInfo:
    _weaponID = ""
    _mod = ""
    _rule = ""
    _penalty = ""

# ------------------------------------------------------------------------ #

class WeaponhandlerPlugin(b3.plugin.Plugin):
    _weaponRestrict = []


    def onStartup(self):
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_CLIENT_DAMAGE)
        self._adminPlugin = self.console.getPlugin('admin')

        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

    def onLoadConfig(self):
        self.debug('Loading Configuration Started')
        for e in self.config.get('weapons/weapon'): 
            _wi = WeaponInfo()
            if e.text:
                _wi._weaponID = e.text
            else:
                _wi._weaponID = ""
                
            _wi._mod = e.get('mod')
            _wi._rule = e.get('rule')
            _wi._penalty = e.get('penalty')
            
            if (_wi._mod != "" or _wi._weaponID != ""):
                self.debug('Weapon restriction loaded: >' + _wi._weaponID + '< Mod:>' + _wi._mod + '<rule:>' + _wi._rule + '<penalty:>' + _wi._penalty + '<')
                self._weaponRestrict.append(_wi)
            else:
                self.debug('Info: Empty settings ignored')        
        self.debug('Loading Configuration Finished')
        return
        

    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_KILL or event.type ==  b3.events.EVT_CLIENT_DAMAGE:
            weaponID = event.data[1]
            mod = event.data[3]
            self.handleWeapon(weaponID, mod, event.client)

    def handleWeapon(self, weaponID, mod, player):
        for weaponInfo in self._weaponRestrict:
            try:
                if weaponInfo._weaponID == weaponID:
                    if weaponInfo._mod == mod:
                        wrule = weaponInfo._rule
                        wpenalty = weaponInfo._penalty
                        if (wpenalty == ""):
                            self.verbose('No penalty defined. Warning player')
                            self._adminPlugin.warnClient(player, wrule , None, False)
                        elif (wpenalty == "warn"):
                            self.verbose('Warning player')
                            self._adminPlugin.warnClient(player, wrule , None, False)
                        elif (wpenalty == "kick"):
                            self.verbose('kicking player')
                            player.kick(wrule, '', none)
            except:
                self.debug('Unknown error occured')  
