import os
import json
from unicurses import *
from collections import OrderedDict

CONFIG_FILE_NAME = "~/.config/shell-menu/.menu_config.json"

ITEM_TYPE_TEXT = 1
ITEM_TYPE_COMMAND = 2
ITEM_TYPE_SUBMENU = 3


class Menu:
  def __init__(self):
    self.parent = None
    self.items = []
    self.selectedIndex = -1
    self.height = 1
    self.width = 1
    self.offset = 0

  def addItm(self, newItem):
    self.items.append(newItem)
    newItem.parent = self
    if (self.selectedIndex == -1) and (newItem.selectable):
      self.selectedIndex = newItem.index
      newItem.isSelected = True
    newItem.y = self.height
    self.height += newItem.rows
    if newItem.width > self.width:
      self.width = newItem.width

  def next(self):
    changedItems = []
    if self.selectedIndex == -1:
      return changedItems
    if self.selectedIndex != -1 and len(self.items) > 0:
      self.items[self.selectedIndex].isSelected = False
      changedItems.append(self.selectedIndex)
    self.selectedIndex += 1
    if self.selectedIndex >= len(self.items):
      self.selectedIndex = 0
    while not self.items[self.selectedIndex].selectable:
      self.selectedIndex += 1
      if self.selectedIndex >= len(self.items):
        self.selectedIndex = 0
    self.items[self.selectedIndex].isSelected = True
    changedItems.append(self.selectedIndex)
    return changedItems

  def previus(self):
    changedItems = []
    if self.selectedIndex == -1:
      return changedItems
    if self.selectedIndex != -1 and len(self.items) > 0:
      self.items[self.selectedIndex].isSelected = False
      changedItems.append(self.selectedIndex)
    self.selectedIndex -= 1
    if self.selectedIndex < 0:
      self.selectedIndex = len(self.items) - 1
    while not self.items[self.selectedIndex].selectable:
      self.selectedIndex -= 1
      if self.selectedIndex < 0:
        self.selectedIndex = len(self.items) - 1
    self.items[self.selectedIndex].isSelected = True
    changedItems.append(self.selectedIndex)
    return changedItems

  def update(self, max_y, window, A_ITM, A_SELECTED):
    selectedItm = self.items[self.selectedIndex]
    if (selectedItm.y + selectedItm.rows - self.offset) > max_y:
      self.offset = (selectedItm.y + selectedItm.rows) - max_y + 3
    if (selectedItm.y - self.offset) < 3:
      self.offset = (selectedItm.y - 3)
    if self.offset < 0:
      self.offset = 0
    self.drawItems(max_y, window, A_ITM, A_SELECTED)

  def drawItems(self, max_y, window, A_ITM, A_SELECTED):
    wclear(window)
    for itm in self.items:
      itm.draw(max_y, window, A_ITM, A_SELECTED)


class Item:
  def __init__(self, text, selectable, content, index):
    self.parent = None
    self.text = text
    self.isSelected = False
    self.selectable = selectable
    self.index = index
    self.content = content
    self.y = 0
    self.width = 1
    self.type = ITEM_TYPE_COMMAND
    if isinstance(self.content, Menu):
      self.content.parent = self
      self.type = ITEM_TYPE_SUBMENU
    if isinstance(self.text, list):
      self.rows = len(self.text)
      self.type = ITEM_TYPE_TEXT
      for line in self.text:
        if len(line) > self.width:
          self.width = len(line)
    else:
      self.rows = 1
      self.width = len(self.text)

  def draw(self, max_y, win, A_ITM, A_SELECTED):
    style = A_ITM
    if self.selectable and self.isSelected:
      style = A_SELECTED
    y = self.y - self.parent.offset
    if (y + self.rows) <= 0:
      return
    if y > max_y:
      return
    if self.type == ITEM_TYPE_TEXT:
      for line in self.text:
        mvwaddstr(win, y, 2, line, color_pair(style))
        y += 1
    elif self.type == ITEM_TYPE_SUBMENU:
      mvwaddstr(win, y, 0, "  [ > " + self.text + " ] ", color_pair(style))
    else:
      mvwaddstr(win, y, 0, "  [ " + self.text + " ] ", color_pair(style))


class Config:
  def __init__(self, path=CONFIG_FILE_NAME):
    self.menu = None
    self.path = os.path.expanduser(path)
    self.data = {}

  def reload(self):
    if os.path.isfile(self.path):
      with open( self.path, "r" ) as file:
        try:
          self.data = json.loads( file.read(), object_pairs_hook=OrderedDict )
        except ValueError as ve:
          self.data = {"Error":["Error parsing json file!","",str(ve)]}
    else:
      self.data = {
        "StartInfo":[
          "Empty menu_config please press c to edit configuration file.",
          " ",
          "Use json syntax as folowed:",
          "  {  } = menu or submenu.",
          "  [  ] = text each string is one line.",
          '  ".." = OS terminal command.',
          '  if a command ends with "&read" the menu will wait for an [Enter] afterwards.'
        ]
      }

  def createMenu(self):
    def MenuFromDict(data):
      menu = Menu()
      index = 0
      for key in data.keys():
        itm = None
        if isinstance(data[key],list):
          itm = Item(data[key], False, None, index)
        elif isinstance(data[key], dict):
          itm = Item(key, True, MenuFromDict(data[key]), index)
        else:
          itm = Item(key, True, str(data[key]), index)
        menu.addItm(itm)
        index += 1
      return menu
    self.menu = MenuFromDict(self.data)


if __name__=="__main__":
  eingabe = Input("Enter \"test\" to test stuff.")
  if eingabe == "test":
    c = Config()
    c.reload()
    c.createMenu()



