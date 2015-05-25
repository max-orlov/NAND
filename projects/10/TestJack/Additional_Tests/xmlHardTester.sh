#!/bin/sh
cd ~/tecs-software-suite-2.5/bin/classes/

echo '====FrogGame.xml====' 
sh /home/maxim/NAND/tools/TextComparer.sh FrogGame.xml FrogGameA.xml

echo '====GameControl.xml====' 
sh /home/maxim/NAND/tools/TextComparer.sh GameControl.xml GameControlA.xml
echo '====in3.xml====' 
sh /home/maxim/NAND/tools/TextComparer.sh in3.xml in3A.xml
echo '====simpleCommentTest.xml====' 
sh /home/maxim/NAND/tools/TextComparer.sh simpleCommentTest.xml simpleCommentTestA.xml
echo '====Surface.xml====' 
sh /home/maxim/NAND/tools/TextComparer.sh Surface.xml SurfaceA.xml
echo '====try2.xml===='
sh /home/maxim/NAND/tools/TextComparer.sh try2.xml try2A.xml
