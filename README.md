ShellMenu
=========
ShellMenu is a fallout 4 inspired Menu system written in python, configured with a single JSON file.

![ShellMenu Screenshot](https://raw.githubusercontent.com/derDere/ShellMenu/resources/page/shellmenu.png)
![Fallout Screenshot](https://raw.githubusercontent.com/derDere/ShellMenu/resources/page/terminal.png)


Dependencies
------------
 - make
 - python3.5 or greater
 - pip for python3.5 or greater
 - unzip
 - wget


Installation
------------
After installing all dependencies use pip to install the package netifaces:

```shell
sudo pip install netifaces
```

Then use make to run the installation:

```shell
sudo make install
```


Usage
-----
To start just run the following command in your terminal:

```shell
shell-menu
```

Within the menu you can open a help prompt using the h key. You can reload using the r key.
You can edit your current config by pressing c and you can execute terminal commands using the t key.
To exit the menu press q or ESCAPE.
You can navigate throu the menu using the arrow keys or W,A,S,D.
Some keys like ENTER, d or KEY_RIGHT have the same functions.
Here is a table of the keylayout:

<html>
<table><tr><th>Key</th><th>Function</th></tr><tr><td>h</td><td>Show Help</td></tr><tr><td>w</td><td rowspan="2">Up</td></tr><tr><td>Arrow Up</td></tr><tr><td>s</td><td rowspan="2">Down</td></tr><tr><td>Arrow Down</td></tr><tr><td>Enter</td><td rowspan="4">Confirm selection</td></tr><tr><td>e</td></tr><tr><td>d</td></tr><tr><td>Arrow Right</td></tr><tr><td>TAB</td><td rowspan="4">Go Back</td></tr><tr><td>a</td></tr><tr><td>BACKSPACE</td></tr><tr><td>Arrow Left</td></tr><tr><td>q</td><td rowspan="3">Exit ShellMenu</td></tr><tr><td>x</td></tr><tr><td>ESCAPE</td></tr><tr><td>t</td><td>Execute command</td></tr><tr><td>c</td><td>Edit configuration</td></tr><tr><td>r</td><td>Reload Menu</td></tr><tr><td>H</td><td>Show --help for selection</td></tr></table>
<html/>


Configuration
-------------
The configuration is stored entirely in a JSON file. The following explanation assumes that you have basic knowledge of the JSON syntax.
If that's not the case have a look at the folowing link: [w3schools JSON syntax](https://www.w3schools.com/js/js_json_syntax.asp)

### Commands

### Text

### Submenu


Origin
------
bla bla bla
