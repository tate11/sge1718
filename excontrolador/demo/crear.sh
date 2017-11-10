#!/bin/bash

echo '<odoo><data>' > demo.xml
# comunidades
cut -d";" -f1,2 pobles.txt | sort -n | uniq | while read c
do
id=$(echo $c | cut -d";" -f1)
nom=$(echo $c | cut -d";" -f2)
echo '<record model="excontrolador.comunity" id="'$id'"><field name="name">'$nom'</field><field name="country" ref="base.es"/></record>' >> demo.xml
done 

# provincias
cut -d";" -f1,3,4 pobles.txt | sort -n | uniq | while read p
do
id=$(echo $p | cut -d";" -f2)
nom=$(echo $p | cut -d";" -f3)
c=$(echo $p | cut -d";" -f1)
echo '<record model="excontrolador.province" id="p'$id'"><field name="name">'$nom'</field><field name="comunity" ref="excontrolador.'$c'"/></record>' >> demo.xml
done 

# pueblos
cut -d";" -f3,6,7 pobles.txt | while read p
do
id=$(echo $p | cut -d";" -f2)
nom=$(echo $p | cut -d";" -f3)
echo -n "$nom "
c="p$(echo $p | cut -d";" -f1)"
echo '<record model="excontrolador.town" id="'$id'"><field name="name">'$nom'</field><field name="province" ref="excontrolador.'$c'"/></record>' >> demo.xml
done 

echo '</data></odoo>' >> demo.xml
