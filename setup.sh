if [ "$1" != "install" ] && [ "$1" != "uninstall" ]
then
  echo use: \"make\"
  exit 1

elif [ "$1" == "install" ]
then
  echo Installing shell-menu

  mkdir -vp /opt/ShellMenu

  cp -fv ./main.py /opt/ShellMenu/main.py
  cp -fv ./my_system.py /opt/ShellMenu/my_system.py
  cp -fv ./objects.py /opt/ShellMenu/objects.py
  cp -fv ./run /opt/ShellMenu/run

  ln -fvs /opt/ShellMenu/run /usr/bin/shell-menu

  exit 0

elif [ "$1" == "uninstall" ]
then
  echo Uninstalling shell-menu

  rm -frv /opt/ShellMenu

  unlink /usr/bin/shell-menu
  exit 0
fi

exit 1
