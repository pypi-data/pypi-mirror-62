# titleWeekTrend
This was originally part of a YouTube video views prediction model. You can use it to get the sum of Google Trends for each word in a news or video title over the past week.

The input string (the title) will be fixed contractions first, then removed punctuation, converted into lowercase, and finally will be processed by a lemmatiazation.

Next, the input title will be split into individual words, and Google Trends for each word in the past week will be crawled and finally a sum will be obtained.
