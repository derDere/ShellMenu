if [ "$1" != "ogo ogo" ]; then
  echo use: \"make\"
  exit 1
fi

mkdir -vp /opt/ShellMenu

cp -fv ./main.py /opt/ShellMenu/main.py
cp -fv ./my_system.py /opt/ShellMenu/my_system.py
cp -fv ./objects.py /opt/ShellMenu/objects.py
cp -fv ./run /opt/ShellMenu/run

ln -fvs /opt/ShellMenu/run /usr/bin/shell-menu
