from objects import *
from unicurses import *
from unicguard import *
import my_system as mySys
import os


class Command:
  def __init__(self, command, read):
    self.command = command
    self.read = read


class App:
  A_ITM = 0
  A_SELECTED = 0
  A_INFO = 0
  A_HELP = 0
  A_TERM_1 = 0
  A_TERM_2 = 0
  
  def __init__(self):
    self.debug = False
    self.reload = False
    self.command = None
    self.sysWinW = 0
    self.sysWinH = 0
    self.sysWin = None
    self.sysPan = None
    self.infoWin = None
    self.infoPan = None
    self.running = True
    self.window = None
    self.panel = None
    self.stdscr = None
    self.config = None
    self.currentMenu = None
    self.lastMax = 0

  def windowDoAction(self):
    global A_ITM, A_SELECTED
    k = getkey(self.window)
    needsUpdate = False
    if self.debug:
      mvwaddstr(self.infoWin,0,0,str(list(k)) + (" "*10))
    if (k == 'q') or (k == "\x1b") or (k == 'x'):
      self.running = False
      return
    if (k == 'c'):
      self.command = Command("nano %s" % CONFIG_FILE_NAME, False)
      self.running = False
      return
    if (k == 'r'):
      self.load()
    if (k == 't'):
      self.showTerminalInput()
    if (k == 'H'):
      self.itemDoAction(self.currentMenu.items[self.currentMenu.selectedIndex], True)
    if (k == 'h'):
      self.showHelpWin()
    if (k == 'e') or (k == "\n"):
      self.itemDoAction(self.currentMenu.items[self.currentMenu.selectedIndex])
    if ((k == '\t') or (k == 'KEY_BACKSPACE')) and (self.currentMenu.parent != None):
      self.createWindow(self.currentMenu.parent.parent)
    if (k == 'w') or (k == "KEY_UP"):
      self.currentMenu.previus()
      needsUpdate = True
    if (k == 's') or (k == "KEY_DOWN"):
      self.currentMenu.next()
      needsUpdate = True
    (max_y,_) = getmaxyx(self.stdscr)
    if self.lastMax != max_y:
      needsUpdate = True
    if needsUpdate:
      self.currentMenu.update(max_y, self.window, A_ITM, A_SELECTED)
    self.moveSystemWin()
    update_panels()
    doupdate()
  
  def showTerminalInput(self):
    global A_TERM_1, A_TERM_2
    (max_y, max_x) = getmaxyx(self.stdscr)
    usr_str = mySys.username()
    machin_str = mySys.machinename()
    dir_str = mySys.currentDir()
    str_len_1 = len(usr_str) + 1 + len(machin_str)
    str_len = len(usr_str) + 1 + len(machin_str) + 1 + len(dir_str) + 2
    w = max_x - 8
    if w <= 0:
      w = max_x
    if w > 80:
      w = 80
    h = 3
    x = 1
    y = 1
    x = round((max_x - w) / 2)
    y = round((max_y - h) / 2)
    tw = newwin(h,w,y,x)
    pan = new_panel(tw)
    box(tw)
    mvwaddstr(tw, 1, 1, "%s@%s" % (usr_str, machin_str), color_pair(A_TERM_1))
    mvwaddstr(tw, 1, 1 + str_len_1, ":")
    mvwaddstr(tw, 1, 1 + str_len_1 + 1, dir_str, color_pair(A_TERM_2))
    mvwaddstr(tw, 1, 1 + str_len - 2, "$")
    update_panels()
    doupdate()
    curs_set(True)
    echo()
    command = mvwgetstr(tw, 1, 1 + str_len).decode()
    noecho()
    curs_set(False)
    if self.debug:
      mvwaddstr(tw,0,0,command.decode())
      wgetkey(tw)
    delwin(tw)
    if len(command) > 0:
      self.command = Command(command, True)
      self.running = False
  
  def showHelpWin(self):
    global A_HELP
    (max_y, max_x) = getmaxyx(self.stdscr)
    w = 49
    h = 18
    x = round((max_x - w) / 2)
    y = round((max_y - h) / 2)
    hw = newwin(h,w,y,x)
    pan = new_panel(hw)
    box(hw)
    wattron(hw, A_BOLD)
    mvwaddstr(hw, 1,2,"HELP:", color_pair(A_HELP))
    wattroff(hw, A_BOLD)
    mvwaddstr(hw, 2,0,"├───────────────────────────────────────────────┤")
    mvwaddstr(hw, 3,2,"h            = Shows Help.", color_pair(A_HELP))
    mvwaddstr(hw, 4,2,"w            = Go up.", color_pair(A_HELP))
    mvwaddstr(hw, 5,2,"[Arrow Up]   = Go up.", color_pair(A_HELP))
    mvwaddstr(hw, 6,2,"s            = Go down.", color_pair(A_HELP))
    mvwaddstr(hw, 7,2,"[Arrow Down] = Go down.", color_pair(A_HELP))
    mvwaddstr(hw, 8,2,"e            = Confirm selection.", color_pair(A_HELP))
    mvwaddstr(hw, 9,2,"[Enter]      = Confirm selection.", color_pair(A_HELP))
    mvwaddstr(hw,10,2,"[tab]        = Go back.", color_pair(A_HELP))
    mvwaddstr(hw,11,2,"[Backspace]  = Go back.", color_pair(A_HELP))
    mvwaddstr(hw,12,2,"q            = Exit application.", color_pair(A_HELP))
    mvwaddstr(hw,13,2,"x            = Exit application.", color_pair(A_HELP))
    mvwaddstr(hw,14,2,"t            = Enter terminal command.", color_pair(A_HELP))
    mvwaddstr(hw,15,2,"c            = Edit configuration.", color_pair(A_HELP))
    mvwaddstr(hw,16,2,"H            = Show help of selected command.", color_pair(A_HELP))
    update_panels()
    doupdate()
    getkey(hw)
    delwin(hw)
  
  def itemDoAction(self, item, showHelp=False):
    if item.type == ITEM_TYPE_SUBMENU:
      self.createWindow(item.content)
    elif item.type == ITEM_TYPE_COMMAND:
      read = False
      command = item.content
      if item.content[-5:] == "&read":
        read = True
        command = command[:-5]
      if showHelp:
        read = True
        command += " --help|more"
      self.command = Command(command, read)
      self.running = False
  
  def createWindow(self, menu):
    global A_ITM, A_SELECTED
    self.currentMenu = menu
    (max_y,_) = getmaxyx(self.stdscr)
    self.lastMax = max_y
    winHeight = menu.height + 1
    if winHeight > (max_y - 2):
      winHeight = max_y - 2
    self.window = newwin(winHeight, menu.width + 9, 2, 0)
    for itm in menu.items:
      itm.draw(max_y, self.window, A_ITM, A_SELECTED)
    self.panel = new_panel(self.window)
    update_panels()
    doupdate()
  
  def createInfoWin(self):
    global A_INFO
    self.infoWin = newwin(1, 42, 1, 2)
    self.infoPan = new_panel(self.infoWin)
    waddstr(self.infoWin, "q = quit, h = help, r = reload, TAB = back", color_pair(A_INFO))
  
  def moveSystemWin(self):
    (max_y,max_x) = getmaxyx(self.stdscr)
    move_panel(self.sysPan, max_y - (self.sysWinH + 1), max_x - (self.sysWinW + 1))
  
  def createSystemWin(self):
    global A_SYSTEM
    usr_str = "%s@" % mySys.username()
    machin_str = mySys.machinename()
    dir_str = mySys.currentDir()
    ips = mySys.getIPs()
    (max_y,max_x) = getmaxyx(self.stdscr)
    h = len(ips) + 4
    w = 15
    if w < len(dir_str):
      w = len(dir_str)
    if w < len(machin_str):
      w = len(machin_str)
    if w < len(usr_str):
      w = len(usr_str)
    self.sysWinW = w
    self.sysWinH = h
    self.sysWin = newwin(h, w, max_y - (h + 1), max_x - (w + 1))
    self.sysPan = new_panel(self.sysWin)
    wattron(self.sysWin, color_pair(A_SYSTEM))
    wattron(self.sysWin, A_DIM)
    y = 0
    for ip in ips:
      mvwaddstr(self.sysWin, y, w - len(ip), ip, color_pair(A_SYSTEM))
      y += 1
    y += 1
    mvwaddstr(self.sysWin, y, w - len(usr_str), usr_str, color_pair(A_SYSTEM))
    y += 1
    mvwaddstr(self.sysWin, y, w - len(machin_str), machin_str, color_pair(A_SYSTEM))
    y += 1
    mvwaddstr(self.sysWin, y, w - len(dir_str), dir_str, color_pair(A_SYSTEM))
  
  def load(self):
    self.reload = False
    self.config = Config()
    self.config.reload()
    self.config.createMenu()
    self.currentMenu = self.config.menu
  
  def run(self):
    global A_ITM, A_SELECTED, A_INFO, A_SYSTEM, A_HELP, A_TERM_1, A_TERM_2
    with unicurses_guard() as stdscr:
      self.stdscr = stdscr
      A_ITM = new_style(COLOR_GREEN, COLOR_BLACK)
      A_SELECTED = new_style(COLOR_BLACK, COLOR_GREEN)
      A_INFO = new_style(COLOR_BLUE, COLOR_BLACK)
      A_SYSTEM = new_style(COLOR_YELLOW, COLOR_BLACK)
      A_HELP = new_style(COLOR_CYAN, COLOR_BLACK)
      A_TERM_1 = A_ITM
      A_TERM_2 = A_INFO
      self.createInfoWin()
      self.createSystemWin()
      self.createWindow(self.currentMenu)
      while self.running:
        self.windowDoAction()
      self.running = True      


def main(argv):
  app = App()
  if "--debug" in argv:
    app.debug = True
    print("Debug ON")
    import time
    time.sleep(2)
  app.load()
  running = True
  while running:
    app.run()
    if app.command == None:
      running = False
    else:
      os.system("clear")
      os.system(app.command.command)
      if app.command.read:
        input()
      app.command = None
      if app.reload:
        app.load()
      


if __name__=="__main__":
  import sys
  if len(sys.argv) > 1:
    main(sys.argv[1:])
  else:
    main([])

