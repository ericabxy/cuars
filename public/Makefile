%.html: %.md
	perl -e 'print "<!DOCTYPE html>\n"' > $@
	perl -e 'print "<html>\n"' >> $@
	perl -e 'print "<head>\n"' >> $@
	perl -e 'print "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />\n"' >> $@
	perl -e 'print "</head>\n\n"' >> $@
	perl -e 'print "<body>\n"' >> $@
	perl Markdown.pl $< >> $@
	perl -e 'print "<hr style=\"clear:both;\">\n"' >> $@
	perl -e 'print "</body>\n"' >> $@
	perl -e 'print "</html>\n"' >> $@
