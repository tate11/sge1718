#!/bin/bash

echo '<odoo><data>' > coches.xml

while read line
do
read image name type categ_id <<< $line
image="$(base64 $image)" 
 echo -e '<record id="'$name'" model="product.template">\n<field name="name">'$name'</field>\n<field name="image_medium">'"$image"'</field>\n<field name="type">'"$type"'</field>\n<field name="categ_id" ref="'"$categ_id"'"></field></record>' >> coches.xml

done < coches.txt


echo '</data></odoo>' >> coches.xml
