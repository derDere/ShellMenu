All:
	@echo run \"sudo make install\" to install ShellMenu

install: subgit unicurses unicguard
	@./install.sh "ogo ogo"
	@echo DONE
	@echo start the menu using the command \"shell-menu\"
	@echo press h inside for help
	@echo you can pass in different config files

subgit:
	git submodule update

unicurses: subgit
	$(cd ./unicguard; ./install_unicurses.sh)

unicguard: subgit unicurses
	$(cd ./unicguard; ./install.sh)
