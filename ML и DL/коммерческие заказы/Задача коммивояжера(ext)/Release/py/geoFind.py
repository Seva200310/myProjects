import openrouteservice
import itertools


class finder():
    def __init__(self,apikey,citylist,mode):
        self.client = openrouteservice.Client(key=apikey)
        self.mode=mode
        self.trevelData={"locations":citylist}
    def main(self):
        self.matrix=self.prepareData()
        self.findBestWay(self.allWays())
        link=self.makeYandexMapsLink()
        return link
    def geocode(self,city):
        client=self.client
        address = city
        geocode = client.pelias_search(
        text=address,
        validate=False,
        )
        return geocode["features"][0]["geometry"]["coordinates"]

    def makeMatrix(self):
        client = self.client
        matrix = client.distance_matrix(
            locations=self.trevelData["coordinates"],
            profile='driving-car',
            units='km',
            metrics=['distance'],
            validate=False,
        )
        #print(coordinates)
        return matrix['distances']
    
    def prepareData(self):
        coordinates=[]
        for city in self.trevelData['locations']:      
            coordinates.append(self.geocode(city))
        self.trevelData["coordinates"]=coordinates
        matrix=self.makeMatrix()
        return matrix
    
    def allWays(self):
        mode=self.mode
        matrix=self.matrix
        points=[]
        for i in range(len(matrix)-1):       
            points.append(i+1)
        allWays = list(itertools.permutations(points))
        if mode==True:
            filteredWays = [way for way in allWays if way[-1]==points[-1]]
            return filteredWays
        else:
            return allWays
        
    def findBestWay(self,ways):
        matrix=self.matrix
        #print(ways)
        waylist=[]
        for way in ways:
            roadLen=matrix[0][way[0]]
            for i in range(len(way)-1):
                roadLen=roadLen+matrix[way[i]][way[i+1]]
            #print(roadLen)
            wayDesc={'way':way,'roadLen':roadLen}
            waylist.append(wayDesc)
        best=waylist[0]
        #print(f'the best is {best}')
        for way in waylist:
            if way['roadLen']<best['roadLen']:
                best=way#['roadLen']
        #print(f'the best is {best}')
        best['way']=[0]+list(best['way'])
        coords=[]
        for index in best['way']:
            coords.append(self.trevelData["coordinates"][index])
        best['coordinates']=coords
        self.best=best
        
        return best
    def makeYandexMapsLink(self):
        coords=self.best["coordinates"]
        #print(f'Это координаты из которых формируется ссылка {coords}')
        pointsLinkPart=''
        for coord in coords:
           pointsLinkPart+=str(coord[1])+'%2C'+str(coord[0])+'~'
        pointsLinkPart=pointsLinkPart[:-1]
        #55.755864%2C37.617698~59.938955%2C30.315644~58.522857%2C31.269816~59.220501%2C39.891523
        link='https://yandex.ru/maps/?from=tabbar&ll='+str(coords[0][1])+'%2C'+str(coords[0][0])+'&mode=routes&rtext='+pointsLinkPart+'&rtt=auto&ruri=ymapsbm1%3A%2F%2Fgeo%3Fdata%3DCgg1MzAwMDA5NBIa0KDQvtGB0YHQuNGPLCDQnNC-0YHQutCy0LAiCg2GeBZCFQEGX0I%2C~~~ymapsbm1%3A%2F%2Fgeo%3Fdata%3DCgg1MzE0OTUwMhIc0KDQvtGB0YHQuNGPLCDQktC-0LvQvtCz0LTQsCIKDeyQH0IVy-FsQg%2C%2C&source=serp_navig&z=5.39'
        link='https://yandex.ru/maps/?from=tabbar&ll='+str(coords[0][1])+'%2C'+str(coords[0][0])+'&mode=routes&rtext='+pointsLinkPart+'&rtt=auto&source=serp_navig&z=5.39'
        return link

'''apikey='5b3ce3597851110001cf62484e7802db91ae467bb71ccb306c00424a'
mode=True
city=['Москва','Грозный','Минск']
url_get=finder(apikey,city,mode)
otvet=url_get.main()
print(otvet)'''


