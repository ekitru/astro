cd $HOME/astro_project
if  [ -d "/home/user/astro_project" ]; then
    echo "remove all"	
    sudo rm -rf /home/user/astro_project/*
else
    echo "creating new folder"
    sudo mkdir  "/home/user/astro_project"	
fi

echo "Start to copy all data"
sudo cp -R . /home/user/astro_project/.
echo "Change owner to user:user"
sudo chown -R user:user /home/user/astro_project
sudo chmod -R 777 /home/user/astro_project
echo "Removing unneeded files"
sudo rm -rf /home/user/astro_project/.idea
sudo rm -rf /home/user/astro_project/.git
sudo rm -rf /home/user/astro_project/.gitignore
sudo rm -rf /home/user/astro_project/astro_project.iml
sudo rm -rf /home/user/astro_project/README
sudo rm -rf /home/user/astro_project/push_new_astro.sh
echo "Done...."

