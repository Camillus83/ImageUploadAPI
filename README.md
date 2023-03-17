## Image Upload API

This is a Django Rest Framework API for uploading and managing images. Users can upload images in PNG or JPG format and view their uploaded images. The API provides thumbnail links of different sizes based on the user's account plan.

## Installation

To run the application:

1. Clone repository

   ```bash
   git clone git@github.com:Camillus83/ImageUploadAPI.git
   ```

2. Install Docker and Docker Compose if not already installed

3.  Run `docker-compose up -d --build `

4. If the application doesn't start on a first time, please run it again with `docker-compose down && docker-compose up -d`

5. The API should be accesible at `127.0.0.1:8000`

6.  Run migrations

   ```bash
   docker-exec -it hexocean-task-web-1 bash
   python manage.py migrate
   ```

7. Create superuser

```bash
docker-exec -it hexocean-task-web-1 bash
python manage.py createsuperuser
```

8. Create some users and assign them roles

   Visit ``127.0.0.1:8000/admin`, create some users and assign them roles.
   
   ![image](https://user-images.githubusercontent.com/87909623/226049871-7301f359-029b-4886-8148-2c114e06d91e.png)


## Api Usage

## Viewing Uploaded Images

Users can view their uploaded images using the following endpoint

```bash
GET /api/v1/images
```

This will return a list of all the user's uploaded images, including the file name and thumbnail links of a different sizes based on the user's account plan.

![image](https://user-images.githubusercontent.com/87909623/226050294-7c13286f-e43e-4f3e-bd3b-69d41100c776.png)


## Uploading an Image

Users can upload an image using the following endpoint

```bash
POST /api/v1/images
```


![image](https://user-images.githubusercontent.com/87909623/226050524-46d340da-eaf0-42d3-aae5-31ca4212a999.png)

## 200px thumbnail preview

![image](https://user-images.githubusercontent.com/87909623/226050631-dbd1c53c-b365-4f04-bf9e-7d8c25856387.png)

## 400px thumbnail preview

![image](https://user-images.githubusercontent.com/87909623/226050675-5089c284-3cbc-41c9-8962-a95afcebce2a.png)

## Original image preview

![image](https://user-images.githubusercontent.com/87909623/226050748-f8eed4af-a2a5-42b9-9619-be660fe5aeb4.png)


## Expiring Link to Image

Users can fetch an expiring link to the image using the following endpoint:

```
POST /api/v1/images/<id>/exp
```

In body user should specify time to expire, it should be between 300 and 30000 seconds.

```
{
	"time_to_expire":"<time_specified_in_seconds>"
}
```

That will return an expiring link for the specified image ID.

![image](https://user-images.githubusercontent.com/87909623/226051178-2f72aacb-cfde-4d4b-9659-5c2c0462d3d2.png)


## Account Tiers

There are three built-in account tiers: Basic, Premium and Enterprise. The following thumbnail links are available based on the user's account plan.

### Basic

* Link to a thumbnail that's 200px in height..

### Premium

* Link to a thumbnail that's 200px in height
* Link to a thumbnail that's 400px in height
* Link to the originally uploaded image

### Enterprise

* Link to a thumbnail that''s 200px in height
* Link to a thumbnail that's 400px in height
* Link to the originally uploaded image

## Admin Configuration

Admins can create arbitrary tiers with configurable thumbnail sizes, presence of the link to the originally uploaded file, and ability to generate expiring links. Admin UI can be accesed via the Django admin panel with `127.0.0.1:8000/admin`.

## Tests

To run the tests, run the following commands:

```bash
docker-exec -it hexocean-task-web-1 bash
python manage.py test
```

## Validation

The API includes validation to ensure that only PNG or JPG files can be uploaded ant that the uplaoded files have unique names.



