import argparse
import json
import yaml

prefix = "sublime"
filename = "sublime-keys.t2c"

faderData = [

              ]

keyData =[

            ('fs',['f11']),
            ('sb', ['ctrl','k']),
            ('1c', ['shift','alt','1']),
            ('2c', ['shift','alt','2']),
            ('3c', ['shift','alt','3']),
            ('comment', ['ctrl','/']),
            ('blockcomment', ['shift','ctrl','/']),
            ('deskright', ['ctrl','alt','right']),
            ('deskleft', ['ctrl','alt','left']),

            




]

encoderData = [


              ]

buttonData = [
              
              ]

data = {
  
  "prefix":prefix,
  "faderData":faderData,
  "encoderData":encoderData,
  "buttonData":buttonData,
  "keyData":keyData
}


with open (filename, 'w') as f:
  yaml.dump(data, f)

  
  
  