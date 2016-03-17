"""
Dummy client for Bubble.

"""

__version__ = '0.0.1'
__author__ = 'E. Yildiz'
__licence__ = 'GPLV3'


from bubble import Bubble

class BubbleClient(Bubble):
    def __init__(self,cfg=None):
        pass

    def pull(self,*a,**k):
        for i in range(143):
            yield {'dummy':"dummy_"+str(i)}

    def push(self,*a,**k):
        return "OK" 

