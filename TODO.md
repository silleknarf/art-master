TODO
====

Front end
- Artist tab
    - Show next target thing to draw, set 30 seconds timer to send to server
    - Implement JS drawing pad
    - Save button
- Critic tab
    - Show next two items to pick
    - Allow the items to be picked

Back end
    - POST round
        create a new round and then returns the round info
    - POST round/{round}/drawing/
        provide the image in the body
    - GET round/{round}/drawing
        returns two images to rate
    - GET round/{round}
        provides the round info including who won
    - POST round/{round}/drawing/{drawing}?rating={rating}
        provide the rating
    - POST user
        create a username
        returns whether it worked or not

Database
    - Set up user table only name based 
    - Set up round table with users and images
    - Set up image table with links to the images and user
    - Set up rating table with image and user