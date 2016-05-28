FeedReader
=================
See our [web site](locahost:8000) for details on the project.





### requirement ###
[twitter bootstrap] included in the project
[django](https://www.djangoproject.com/download/)
[python](https://www.python.org/downloads/)
[Mysql](https://www.mysql.com/downloads/)installed.

### Dependencies ###
    pip install mysqldb  

###Four entities in DB###
users [id, username, first_name, last_name, password]
Feed [id, creator, name, url]
Articles[id, title,content,timestamp,Feed]
FeedToSubscribers[id, Feed,Users]

###Media Type###
Json only

###Apps###
Login : mainly deal with login issue.
Feed  : All functionalities, will be explained in detail in modules tag.

###modules###
    All handling will be return in [Json] format.
    Login:
        signup            : mainly signup a user. JS applied.
        password Change   : can allow user to change password
        sign In           : allow user signin and record in session

    Feed:
        POST: 
            Subscribe: 
                subscribe a user to a feed existed:
                    Can allow user to subscribe any feeds including the user's own feeds.
                Error handling:
                    wrong credentials.
                    un-available feed name.
                    duplicate subscription.
                    Exception handling will return invalid request if exception occurred. 
            Unsubscribe: 
                unsubscribe a user to a feed existed:
                    Can allow user to unsubscribe any feeds including the user's own feeds.
                Error handling:
                    wrong credentials.
                    un-available feed name.
                    duplicate unsubscription.
                    Exception handling will return invalid request if exception occurred. 

            Add Article:
                Add article to current user's feed. Can't add article to other user's feed. 
                Error handling:
                    wrong credentials.
                    un-available feed name.
                    duplicate title and content is allowed.
                    Exception handling will return invalid request if exception occurred.

            Add Feed:
                user can add feed as creator.
                Error handling:
                    wrong credentials.
                    un-available feed name.
                    duplicate feed is NOT allowed.

        GET:
            Get Feeds:
                Get all feeds a user subscribed. 
                Error handling:
                    wrong credentials.
                    empty feed. 
                    WRONG post request.
            Get Articles:
                Get all ariticles a user subscribed from feeds. 
                Error handling:
                    wrong credentials.
                    empty feed. 
                    empty aritles set.
                    WRONG post request.

###Chanllenge###
    Short time provided: 
        9 hours development in total
    Edge cases: 
        May miss some edge cases by giving vogue json response when handling exceptions.
    Test:
        Testing takes 20% time of whole process. But It's still not enough.

###Improvement in the future###
    Code refactor : 
        Redundent code found.
    Performance   : 
        Planned to use redis to cache all articles of one user. Because of short development time, this is not involved. 
    JSON API:
        Only key functionalities are dealt with JSON Restful api. Should include more like login module.
    Https:
        Https is supposed to be added. 
    FrontEnd format:
        Json response is not formatted as user friendly.
    FrontEnd display:
        Should display everything in one page. In order to make test clearly, I seperate everything in different pages.
    Framework:
        Django Rest Framework is superb tool for API. Re-invent the wheel is not always encouraged. 
    





