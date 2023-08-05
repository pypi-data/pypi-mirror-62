'''
     MIT License

     Copyright (c) 2020 Stephan Traub

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the "Software"), to deal
     in the Software without restriction, including without limitation the rights
     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
     copies of the Software, and to permit persons to whom the Software is
     furnished to do so, subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
     SOFTWARE.
'''
import socket
import json

class wizlight:
    '''
        Creates a instance of a WiZ Light Bulb
    '''

    UDP_PORT = 38899
    SCENES = {
                1:"Ocean",
                2:"Romance",
                3:"Sunset",
                4:"Party",
                5:"Fireplace",
                6:"Cozy",
                7:"Forest",
                8:"Pastel Colors",
                9:"Wake up",
                10:"Bedtime",
                11:"Warm White",
                12:"Daylight",
                13:"Cool white",
                14:"Night light",
                15:"Focus",
                16:"Relax",
                17:"True colors",
                18:"TV time",
                19:"Plantgrowth",
                20:"Spring",
                21:"Summer",
                22:"Fall",
                23:"Deepdive",
                24:"Jungle",
                25:"Mojito",
                26:"Club",
                27:"Christmas",
                28:"Halloween",
                30:"Candlelight",
                31:"Goldenwhite",
                32:"Pulse",
                33:"Steampunk"
    }

    def __init__ (self, ip):
        ''' Constructor with ip of the bulb '''
        self.ip = ip

    @property
    def scene(self):
        ''' get the current scene name'''
        id = self.getState()['result']['sceneId']
        if id in self.SCENES:
            return self.SCENES[id]
        else:
            return None

    @scene.setter
    def scene(self, scene_id):
        if scene_id in self.SCENES:
            message = '{"method":"setPilot","params":{"sceneId":%i}}' % scene_id
            self.sendUDPMessage(message)
        else:
            pass

    @property
    def color(self):
        ''' get the rgbW color state of the bulb and turns it on'''
        resp = self.getState()
        if "temp" not in resp['result']:
            r = resp['result']['r']
            g = resp['result']['g']
            b = resp['result']['b']
            w = resp['result']['w']
            return r, g, b, w
        else:
            # no RGB color value was set
            return None, None, None, None

    @color.setter
    def color(self, color=(0,0,0,0)):
        ''' set the rgbw color state of the bulb '''
        r, g, b, w = color
        message = r'{"method":"setPilot","params":{"r":%i,"g":%i,"b":%i,"w":%i}}' % (r,g,b,w)
        self.sendUDPMessage(message)
        
    @property
    def rgb(self):
        ''' get the rgb color state of the bulb and turns it on'''
        resp = self.getState()
        if "temp" not in resp['result']:
            r = resp['result']['r']
            g = resp['result']['g']
            b = resp['result']['b']
            return r, g, b
        else:
            # no RGB color value was set
            return None, None, None

    @rgb.setter
    def rgb(self, values):
        ''' set the rgb color state of the bulb '''
        r, g, b = values
        message = r'{"method":"setPilot","params":{"r":%i,"g":%i,"b":%i}}' % (r,g,b)
        self.sendUDPMessage(message)

    @property
    def brightness(self):
        ''' gets the value of the brightness 0-255 '''
        return self.percent_to_hex(self.getState()['result']['dimming'])

    @brightness.setter
    def brightness(self, value=255):
        ''' set the value of the brightness 0-255 '''
        percent = self.hex_to_percent(value)
        # lamp doesn't supports lower than 10%
        if percent > 10:
            message = r'{"method":"setPilot","params":{"dimming":%i}}' % percent
            self.sendUDPMessage(message)
    
    @property
    def colortemp(self):
        resp = self.getState()
        if "temp" in resp['result']:
            return resp['result']['temp']
        else:
            return None

    @colortemp.setter
    def colortemp(self, kelvin):
        ''' sets the color temperature for the white led in the bulb '''
        # normalize the kelvin values - should be removed
        if kelvin < 2500: kelvin = 2500
        if kelvin > 6500: kelvin = 6500 
        
        message = r'{"method":"setPilot","params":{"temp":%i}}' % kelvin
        self.sendUDPMessage(message)
           


    ## ------------------ Non properties --------------
    @property
    def status(self):
        ''' returns true or false / true = on , false = off '''
        return self.getState()['result']['state']

    def turn_off(self):
        ''' turns the light off '''
        message = r'{"method":"setPilot","params":{"state":false}}'
        self.sendUDPMessage(message)

    def turn_on(self):
        message = r'{"method":"setPilot","params":{"state":true}}'
        self.sendUDPMessage(message)

    ### ---------- Helper Functions ------------
    def getState(self):
        '''
        getPilot - gets the current bulb state - no paramters need to be included
        {"method": "getPilot", "id": 24}
        '''
        message = r'{"method":"getPilot","params":{}}'
        return self.sendUDPMessage(message)

    def getBulbConfig(self):
        ''' returns the configuration from the bulb '''
        message = r'{"method":"getSystemConfig","params":{}}'
        return self.sendUDPMessage(message)
    
    def lightSwitch(self):
        '''
        turns the light bulb on or off like a switch
        '''
        # first get the status
        result = self.getState()
        if result['result']['state']:
            # if the light is on - switch off
            self.turn_off()
        else:
            # if the light is off - turn on
            self.turn_on()
    
    def getConnection(self):
        ''' returns true or false and indicates the connection state '''
        try:
            self.getState()
            return True
        except OSError:
            return False


    def sendUDPMessage(self, message):
        ''' send the udp message to the bulb '''
         # fix port for Wiz Lights
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(bytes(message, "utf-8"), (self.ip, self.UDP_PORT))
        sock.settimeout(10.0)
        data, addr = sock.recvfrom(1024)
        if len(data) is not None:
            resp = json.loads(data.decode())
            if "error" not in resp:
                    return resp
            else:
                # exception should be created
                raise ValueError(resp)

    def hex_to_percent(self, hex):
        return round((hex/255)*100)

    def percent_to_hex(self, percent):
        return round((percent / 100)*255)