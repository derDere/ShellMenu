All:
	@echo run \"sudo make install\" to install ShellMenu

.PHONY: uninstall install

install: .a57z6s_runinstallatation
	@echo DONE
	@echo start the menu using the command \"shell-menu\"
	@echo press h inside the menu for help

.a4g6fg_subgit:
	@echo Loading git submodules
	git submodule update

.ytjk75_unicurses: .a4g6fg_subgit
	@echo Installing unicurses
	cd ./unicguard; bash ./install_unicurses.sh

.467sra_unicguard: .a4g6fg_subgit .ytjk75_unicurses
	@echo Installing unicguard
	cd ./unicguard; bash ./install.sh

.a57z6s_runinstallatation: .a4g6fg_subgit .ytjk75_unicurses .467sra_unicguard
	@echo Running menu installation
	bash ./setup.sh install

uninstall:
	@echo Running menu deinstallation
	bash ./setup.sh uninstall
