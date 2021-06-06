# cs257-s21-team-f
Members: Kiefer Lord, Emmy Belloni and Nina Sun
*Kai Maruyama was a part of the group for the first two deliverables.

Database username: bellonie
Database password:recycle368bird

The starting page is the default route.

The only current bug is an issue where the counts of the graph are occasionally off by one. Originally this resulted in an unnamed(null data) extra color of size 1 along the bottom of each column. We got rid of this by appending 0 instead of 1 when a new x variable is found. This currently results in there being tick marks for variables but no bar there, since the height is 0 instead of one.
We are unsure what causes this bug, but since it decrements everything by one, it does not skew the data, and we chose to leave it like this instead of with the extra null bar because it is less distracting from the data.