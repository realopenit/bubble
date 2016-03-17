from bubble import Bubble
class BubbleClient(Bubble):
    def __init__(self,cfg={}):
        self.CFG=cfg
    def pull(self, *args, **kwargs):
        self.say('pull:args:',stuff=args)
        self.say('pull:kwargs:',stuff=args)
        return  [{"id":"1","name":"me:first"},
                 {"id":"2","name":"my:first"}
                ]
