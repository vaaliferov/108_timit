#!/usr/bin/env bash

NAME=timit
USER=ubuntu

DIR=/opt/$NAME
SERVICE_NAME="${NAME}_bot.service"
SERVICE_FILE_PATH=/etc/systemd/system/$SERVICE_NAME

rm -rf $DIR $SERVICE_FILE_PATH
systemctl disable --now $SERVICE_NAME

cat bot.service > $SERVICE_FILE_PATH
sed -i "s/<name>/$NAME/g" $SERVICE_FILE_PATH
sed -i "s/<user>/$USER/g" $SERVICE_FILE_PATH

mkdir $DIR $DIR/env
apt install -y libsndfile1 python3-pip python3-venv
pip3 install virtualenv gdown
python3 -m venv $DIR/env

source $DIR/env/bin/activate
pip3 install --no-cache-dir cython wheel
pip3 install --no-cache-dir -r requirements.txt
deactivate

cp -r . $DIR
gdown --id 1VTEsfOMCGBbhyhWtQitsRzN9dW5UUyIy -O $DIR/timit.zip
unzip -q $DIR/timit.zip -d $DIR

chmod 755 $DIR
chown -R $USER:$USER $DIR

systemctl daemon-reload
systemctl enable --now $SERVICE_NAME