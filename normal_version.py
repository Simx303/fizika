
class Vektoras:
    x=0
    y=0
    v=0
    alpha=0
class Objektas:
    y=0
    x=0
    v=Vektoras()
class Erdve:
    objektai=[]
    def pridet_obj(self, obj):
        self.objektai.append(obj)
    def judit(self, dt):
        for obj in self.objektai:
            obj.x = obj.x + obj.v.x
            obj.y = obj.y + obj.v.y

a = Objektas()
a.v.y = 3
zeme=Erdve()
zeme.pridet_obj(a)
for i in range(200):
    zeme.judit(1)
    print(a.y)
