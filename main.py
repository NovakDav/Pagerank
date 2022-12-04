import validators
import requests
from bs4 import BeautifulSoup

#Funkci pagerank jsem vytvořil z vysvětlní ve videu https://www.youtube.com/watch?v=P8Kt6Abq_rM
#Pagerank se tudíž lehce liší

#Funkce, která má parametr url, ze které chceme získat všechny odkazy , vrací nám pole ve varu [odkaz kde hledáme , naleznutý pdkaz]
def crawler(url):
    main_url = url
    grab = requests.get(main_url)
    soup = BeautifulSoup(grab.text, 'html.parser')

    urls = []
    for link in soup.find_all("a"):
        data = link.get('href')
        if data != None:
            valid = validators.url(data)
            if valid == True:
                url = [main_url, data]
                urls.append(url)

    return urls

#funkce pro výpočet page ranku, b -> vstupní matice , number_of_iterations_ -> počet kolikrát chceme iterovat
def pagerank(b,number_of_iteratiorns):

    members = []
    #vytvoření pole jednotlivých neduplicitních prvků z matice b
    for i in range (0,len(b)):
        members.append(b[i][0])
        members.append(b[i][1])
    members = list(dict.fromkeys(members))

    #vytvoření 2d pole ve tvaru [číslo, kolikrát někam odkazuje]
    count_m = []
    for i in range(0,len(members)):
        count=0
        for j in range(0,len(b)):
            if(b[j][0]==members[i]):
                count+=1
        count_m.append([members[i],count])

    #2d pole obsahující záznam který uzel odkazuje na daný uzel
    #indexováno je podle pole members tudíž hodnota links_b[0] == members[0]
    links_b = []
    for i in range(0,len(members)):
        links_b.append([])
        for j in range(0,len(b)):
            if(members[i]==b[j][1]):
                links_b[i].append(b[j][0])

    #vypočtení první iterace pomocí 1/N
    first_iter = []
    for i in range(0,len(members)):
        first_iter.append(1/len(members))

    #vytvoření kopie pole první iterace abychom si ji v průběhu nepřepisovali
    x = first_iter.copy()

    #výpočet jednotlivých iterací
    for k in range(0,number_of_iteratiorns):
        for i in range(0,len(members)):
            score = 0
            for j in range(0,len(links_b[i])):
                link=links_b[i][j]
                score += first_iter[link-1]/count_m[link-1][1]
            x[i]=score
        first_iter=x.copy()

    return first_iter

#funkce, která nám vytvoří místo {url -> url} tvar {unikátní číslo -> unikátní číslo}
def make_number_map(y):
    unique_y = []
    indexed_unique = []

    #vytvoření z 2d pole, pole jednorozměrné
    for i in range(0,len(y)):
        unique_y.append(y[i][0])
        unique_y.append(y[i][1])

    #odstraníme duplicitní hodnoty a vytvoříme 2d pole ve tvaru [ neduplicitní url , číslo za které jej budeme nahrazovat]
    unique_y = list(dict.fromkeys(unique_y))
    for i in range(0,len(unique_y)):
        indexed_unique.append([unique_y[i],i+1])

    #hodnoty v poli, převzatém v parametru funkce zaměníme za unikátní hodnoty
    for i in range(0,len(y)):
        for j in range(0,len(indexed_unique)):
            if y[i][0]==indexed_unique[j][0]:
                y[i][0]= indexed_unique[j][1]
            if y[i][1]==indexed_unique[j][0]:
                y[i][1]= indexed_unique[j][1]

    return y


a = crawler('https://ailab.fai.utb.cz/')
b= [[1,2],[1,3],[2,4],[3,1],[3,2],[3,4],[4,3]]


#provedeme zanoření
for i in range(0,len(a)-1):
    get_url = a[i][1]
    a += crawler(get_url)

#vymažeme duplicitní odkazy
*y,=map(list,{*map(tuple,a)})

print("Pagerank vzorových dat:")
print( pagerank(b,50))

print("Dataset:" )
print(y)
numbered_y=make_number_map(y)
print("Dataset převedený do číselné podoby:")
print(numbered_y)
print("Pagerank datasetu:")
print(pagerank(numbered_y,50))





