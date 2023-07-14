%.html: %.md
	echo '<!DOCTYPE html>' > $@
	echo '<html>' >> $@
	echo '<head>' >> $@
	echo '<link rel="stylesheet" type="text/css" href="style.css" />' >> $@
	echo '</head>' >> $@
	echo '' >> $@
	echo '<body>' >> $@
	markdown $< >> $@
	echo '<hr style="clear:both;">' >> $@
	echo '</body>' >> $@
	echo '</html>' >> $@
