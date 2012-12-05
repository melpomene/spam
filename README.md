BAYESIAN SPAM DETECTOR
======================

Bayes'ed (hehe) on the ideas from [Paul Grahams spam detector](http://www.paulgraham.com/spam.html).  


The script depends on a sqlite database named 
    spam.db

with the following schema

    CREATE TABLE comments 
    (
        spam_id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment varchar(500),
        spam INTEGER
    );

If the spam integer is set to one it is counted as spam. 

Currently the filter retrains on the set everytime it wants to check a input for spam risk. This is obviously not a good way but I have kept it that way during the development since I am still inthe processess of traing to find good training data. 

If you have suggestions please feel free to contact me. 

