This dataset contains two files, IDE_data.csv and points.csv

IDE_data.csv contains IDE logs from the first part of an introductory programming course.

The IDE logs consist of an anonymized student identifier (identifier matches points.csv), information on which event happened (brief explanations of the events below), which exercise was the event related to, and how long before the deadline the event happened (in seconds). There is one row in the data for each event that was logged.

There were 29 exercises in the first part of the course, the number of the exercise indicates the order of the exercises.

There are seven types of events in the IDE data:
- text_insert: text was added into the IDE (at the keystroke level)
- text_remove: text was removed from the IDE
- text_paste: text was pasted into the IDE
- focus_gained: the IDE gained focus (student clicked into the IDE)
- focus_lost: the IDE lost focus (student clicked away from the IDE)
- run: student ran their program
- submit: student submitted their program

points.csv contains the number of points (as a percentage of the maximum) that students got in the seven different parts of the course and a revision round where they could score bonus points. The points are floored to the closest 10%, so e.g. a student who had 57% of the points for a certain part will have 0.5 as their points in the data for that part.

This course version did not have computerized exams (only pen and paper) so unfortunately points for the exams are not available. As a proxy, perhaps you could consider the points from the last part (part 7).

Notes:
Please do not push the data to public repositories (e.g. GitHub).

Only students who consented to research are included in the data.

Only students who had at least 100 IDE log events are included in the data.

The data only includes students who gained at least 25% of the points in the first part to match the data filtering used for the other (MOOC) dataset.

The students could run unit tests locally on their computer (not logged) due to which many students only have a single submission event for each exercise (they only submit after the tests pass locally).

Contrary to the MOOC dataset, the students had less time to work on the exercises (around a week).

Some students might not have many IDE logs even if they have a lot of points -- it's possible they partly worked offline and logs were never sent to the server or they might have returned assignments through a web-UI instead of through the IDE.

Contact for any questions:
juho.leinonen@helsinki.fi
