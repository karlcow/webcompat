# Makefile to create markup for Weekly Web compat report
#

OPENED = /tmp/moz-openedbug.txt
CLOSED = /tmp/moz-closedbug.txt
CLEANDATA = grep -v "\[meta\]" | grep -v "^\"Bug ID" | sed -E 's,\[,\(,g'|sed -E 's,\],\),g'
PYTHON = /usr/bin/python

fetchdata:
	http GET "https://bugzilla.mozilla.org/buglist.cgi?bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&chfield=%5BBug%20creation%5D&chfieldfrom=-8d&chfieldto=Now&component=Mobile&list_id=8332099&product=Tech%20Evangelism&query_format=advanced&ctype=csv&human=1&columnlist=bug_id,opendate,short_desc" > $(OPENED)
	http GET "https://bugzilla.mozilla.org/buglist.cgi?bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&chfield=cf_last_resolved&chfieldfrom=-8d&chfieldto=Now&columnlist=bug_id%2ccf_last_resolved%2Cshort_desc%2Cresolution&component=Mobile&list_id=8332306&product=Tech%20Evangelism&query_format=advanced&resolution=FIXED&resolution=INVALID&resolution=WONTFIX&resolution=WORKSFORME&ctype=csv&human=1" > $(CLOSED)

open:
	cat  $(OPENED) | sort -n -t"," -k2 | $(CLEANDATA) \
	| sed -E 's,^([0-9]+)\,"(....-..-..).*"\,"(.*)",* [https://bugzilla.mozilla.org/show_bug.cgi?id=\1 \3] \2,'

closed:
	cat $(CLOSED) | $(CLEANDATA) \
	| sed -E 's,^([0-9]+)\,"(....-..-..).*"\,"(.*)"\,"(.*)",* [https://bugzilla.mozilla.org/show_bug.cgi?id=\1 \3] \2 \4,' | grep -v meta

feed:
	$(PYTHON) extractfeedtitle.py

clean:
	rm $(OPENED) $(CLOSED)

report: open closed feed
