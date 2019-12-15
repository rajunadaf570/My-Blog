# My Blog
## Requirements:
1. Python 3.7
2. virtualenv
### Step 1: Create virtualenv and Install requirements.txt file.
    virtualenv -p python3.7 {env_name}
    pip install -r requirements.txt
 Active the virualenv.
### Step 2: Create Migration file, Execute migrations and Run the Application
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

### Create User 
    python manage.py createsuperuser
    
## Api request and response
#### Login user
    curl -X POST \
          http://127.0.0.1:8000/api-token-auth/ \
          -d '{
             "username":"{enter username}",
            "password":"{password}"
             }'
     Response:
       {
           "token": "4bcb0439356a53a577355abe01d42d39428b0e89"
       }
#### Post the Blog
        curl -X POST \
          http://127.0.0.1:8000/api/v1/blog/post/ \
          -H 'Authorization: token {token}' \
          -d '{
            "title":"{title name}",
            "content":"{body}.",
            "status":"P"
            }'
#### My Blogs
    curl -X GET \
      http://127.0.0.1:8000/api/v1/blog/mybloglist/ \
      -H 'Authorization: token {token}' 
#### Delete my Blog
        curl -X DELETE \
          http://127.0.0.1:8000/api/v1/blog/deleteblog/ \
          -H 'Authorization: token {token}' \
          -d '{
                 "id":"{blog id}"
              }'
####  To list the Blogs with total_likes, total_dislike, total_comment and total_views for the perticular blog with Pagination
    curl -X GET \
      http://127.0.0.1:8000/api/v1/blog/listofblogs/ \
      -H 'Authorization: token {token}' \
#### To like the perticular Blog
    curl -X POST \
      http://127.0.0.1:8000/api/v1/blog/like/ \
      -H 'Authorization: token {token}' \
      -d '{
         "id": "{blog_id}"
    }
     Response:
       {
          "status": "ok"
       }
#### To dislike 
    curl -X POST \
      http://127.0.0.1:8000/api/v1/blog/dislike/ \
      -H 'Authorization: token {token}' \
      -d '{
      "id": "{blog_id}"
    }'
     Response:
       {
          "status": "ok"
       }
#### To get the Blog and this api increament the number of views.
        curl -X GET \
          http://127.0.0.1:8000/api/v1/blog/getblog/ \
          -H 'Authorization: token {token}' 
            "id":"{blog_id}"
        }'
#### Comment to the Blog
    curl -X POST \
          http://127.0.0.1:8000/api/v1/comment/postcomment/ \
          -H 'Authorization: token {token}' \
          -d '{
            "id":"{blog_id}",
            "comment":"{comment}./"
        }'
#### List a blog Comments
        curl -X GET \
          http://127.0.0.1:8000/api/v1/comment/listcomment/ \
          -H 'Authorization: token {token}' \
          -d '{
            "id":"{blog_id}"
        }'
#### Delete the Comment
         curl -X DELETE \
          http://127.0.0.1:8000/api/v1/comment/deletecomment/ \
          -H 'Authorization: token {token}' \
          -d '{
            "id":"{comment_id}"
        }'
    Response:
       {
        "detail": "deleted successfully."
      }
#### Blogs Details will display the who all commented liked and disliked the Blogs.
        curl -X GET \
          http://127.0.0.1:8000/api/v1/blog/blogsdetails/ \
          -H 'Authorization: token {token}' \
