
# coding: utf-8

# In[64]:

from bs4 import BeautifulSoup
from bs4 import Comment
import urllib.request


# In[65]:

class FoodItem:
    def __init__(self, name, price, description, menuGroup):
        self.name = name
        self.price = price
        self.description = description
        self.menuGroup = menuGroup

    def debugPrint(self):
        print(self.name,' \tCOST ',self.price, '\n',self.description,'\n', self.menuGroup)
        print(' ---- ')


# In[66]:

def loadInitialMenu(restaurantName):
    restaurantName = '+'.join(restaurantName.split())
    searchQuery = restaurantName + "+" + "menu"
    url = "https://www.bing.com/search?q=" + searchQuery
    response = urllib.request.urlopen(url)
    return response.read()


# In[67]:

def parseInitialMenu(html):
    soup = BeautifulSoup(html, 'html.parser')
    # data we need is all in div with class "b_ans b_top b_topborder"
    menuHtml = soup.find("li", class_="b_ans b_top b_topborder")

    if menuHtml is None:
        exit()
    return menuHtml.find("div", class_="tab-container")

def parseMenuGroups(menuHtml):
    menuHeaders = menuHtml.find("div", class_="tab-head")
    menuHeaders = menuHeaders.find("div", class_="tab-menu tab-hasnav")
    menuHeaders = menuHeaders.find_all('li')
    return [item.text for item in menuHeaders]

def parseMenuItems(menuHtml,menuHeaders,isInitial):
    menu = {}
    if isInitial:
        startIndex = 0
        menuContent  = menuHtml.find("div", class_="tab-content")
        menuContent = menuContent.select('div[id^="tab_"]')
    else:
        startIndex = 6
        menuContent = menuHtml.select('div[id^="rcontent_"]')

    for i in range(startIndex,len(menuContent)):
    # for i in range(0,3):
        groupedItems = menuContent[i]
        groupedItemsHtml = groupedItems.find_all('div',class_='tdif')
        menuGroup = menuHeaders[i]
        for item in groupedItemsHtml:
            (name,price) = getItemNamePrice(item)
            description = getItemDesc(item)

            if name not in menu:
                # notice how menuGroup parameter is a list
                foodItem = FoodItem(name,price,description,[menuGroup])
                menu[name] = foodItem
            else:
                foodItem = menu[name]
                if menuGroup not in foodItem.menuGroup:
                    foodItem.menuGroup.append(menuGroup)
    return menu


# In[68]:

def getRestaurantId(html):
    soup = BeautifulSoup(html, 'html.parser')
    comments=soup.find_all(string=lambda text:isinstance(text,Comment))
    for c in comments:
        if 'tabCount' in c:
            x = c.split('tabCount')
            if len(x) <= 1:
                break
            x = x[1].split(',')
            x = x[-1].split('"')
            print(x[1])
            return x[1]
    return ''


def getTabCount(menuHeaders):
    return len(menuHeaders)

def loadAdditionalMenu(html):
    restid = getRestaurantId(html)
    if restid  is '':
        return
    tabCount = getTabCount(html)
    url = 'http://www.bing.com/local/menu?tabCount=' + str(tabCount) + '&tabStart=6&othersTab=0&ypid='+ restid
    response = urllib.request.urlopen(url)
    return response.read()

def parseAdditionalMenu(html,menuHeaders):
    additionalHtml = loadAdditionalMenu(html)
    if additionalHtml is None:
        return
    soup = BeautifulSoup(additionalHtml, 'html.parser')
    parseMenuItems(soup,menuHeaders,isInitial=False)


# In[ ]:

def getItemNamePrice(item):
    itemName = ''
    itemPrice = ''
    h4 = item.find('h4')
    if h4:
        if len(h4.contents) > 0:
            itemName = h4.contents[0]
        if len(h4.contents) > 1:
            itemPrice = h4.contents[1].contents[0]
    return itemName, itemPrice

def getItemDesc(item):
    itemDescription = ''
    span = item.find('span',class_='b_demoteText')

    if span and len(span.contents) > 0:
        itemDescription = span.contents[0]
    return itemDescription


# In[109]:

def getMenu(restaurantName):
    html = loadInitialMenu('il Tramezzino menu')

    menuHtml = parseInitialMenu(html)
    menuHeaders = parseMenuGroups(menuHtml)
    menu = parseMenuItems(menuHtml, menuHeaders, isInitial=True)
    parseAdditionalMenu(html,menuHeaders)
    return menu
# In[110]:


# restaurants that you can try
# - ghirardelli chocolate company
# - palomino
# - il Tramezzino
# - oxnard coffee shop
#menu = {}
#print(getMenu('il Tramezzino'))

# In[112]:

# for item in menu:
#     print(menu[item].debugPrint())

