%.html: %.md
	perl -e 'print "<!DOCTYPE html>\n"' > $@
	perl -e 'print "<html lang=\"en-us\">\n"' >> $@
	perl -e 'print "<head>\n"' >> $@
	perl -e 'print "<title>\n"' >> $@
	perl -e 'print "Command Utility Access and Retrieval System\n"' >> $@
	perl -e 'print "</title>\n"' >> $@
	perl -e 'print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"' >> $@
	perl -e 'print "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />\n"' >> $@
	perl -e 'print "</head>\n\n"' >> $@
	perl -e 'print "<body>\n"' >> $@
	perl Markdown.pl $< >> $@
	perl -e 'print "</body>\n"' >> $@
	perl -e 'print "</html>\n"' >> $@
