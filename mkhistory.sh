# file: mkhistory.sh
# vim:fileencoding=utf-8:fdm=marker:ft=sh
#
# Copyright © 2022 R.F. Smith <rsmith@xs4all.nl>
# SPDX-License-Identifier: MIT
# Created: 2022-04-15T22:48:16+0200
# Last modified: 2022-05-26T18:06:25+0200
echo "% vim:fileencoding=utf-8:ft=tex"
echo "% Automatically generated by mkhistory.py"
echo
echo "\\begin{tabbing}"
HASHSZ="1.5cm"
MSGSZ="6.7cm"
NAMESZ="2.5cm"
echo "\hspace*{${HASHSZ}}\=\hspace{${MSGSZ}}m\=\hspace{${NAMESZ}}\=mmmm-mm-mm\kill"
git log --date=short \
    --pretty=format:"\\textsc{%h} \> \parbox[t]{${MSGSZ}}{%s} \> %an \> %ad\\\\[2pt]"
echo "\\end{tabbing}"