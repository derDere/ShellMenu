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
If you want to add a command option to your menu (for example opening htop) you just have to add a key with a string value to your JSON object.
The key will be shown inside the menu and the string value will be the command executed.

```json
"Open htop": "htop"
```

After completing the execution of the command the menu will reopen by default.
If you wish the command to wait until you press enter end the command with the string ```&read``` all lowercase no whitespaces.

```json
"Show Datetime": "date&read"
```

### Text
If you want to add text to a menu just add a key with an array value containing each line of text as a string value.
The content of the key will not be displayed so its content doesn't realy matter, it just has to be unique.
If the key is not unique that will override the previous one. (I just add a number counting up each time.)

```json
"T1": [
    "Text Line 1",
    "Text Line 2"
],
"T2": [
    "Another Line of text"
}
```

Do not use new line characters to create new lines rather than just a new string value to prevent displaying errors!

### Submenu
Creating a submenu is simple just add a key with an object value containing more keys. The key will be the title displayed in the parent menu,
and the content of the object will be used to display the submenu.

```json
"Open Submenu": {
    "T1": [ "Submenu Title" ],
    "Submenu Option": "echo Hello&read"
}
```

If you want to see all examples used in one config file take a look at "examples/readme_example.json".


Origin
------
Before I was a Linux fan, I was a bit put of by the use of the terminal. Mainly bacause I wasn't compfy using it.
But I still wanted to get into Linux and a lot of my dev friend where using Ubuntu.
So what I did was: I installed Ubuntu Server Edition on one of my old Laptops, forcing me to only use the terminal.
After hours of tinkering around to get the freaking wifi to work I started to look at curses/terminal based applications.
So after finding some applications like wicd-curses, ranger, pulsemixer and gotop, I wanted a way to acces them easely.
And as a developer, who was currently playing the Fallout 4 game, I took the for me quickest aproach and just recreated
the TUI from the Fallout Terminals. I was quite happy so far and now after a few years of ignoring this litte project
I decided to revive it and tidy it up for others to enjoy.

I am planing on creating a faster more customizable version using c++ in the future. And for some fun I will also recreate the
fallout hacking minigame, at least if no one has already done so. Have fun using this Version, I am open for sugjestios for the versoin 2.0.
I won't be changing this old one up to much tho.
