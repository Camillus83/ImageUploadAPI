## Image Upload API

This is a Django Rest Framework API for uploading and managing images. Users can upload images in PNG or JPG format and view their uploaded images. The API provides thumbnail links of different sizes based on the user's account plan.

## Installation

To run the application:

1. Clone repository

   ```bash
   git clone
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

## Api Usage

## Viewing Uploaded Images

Users can view their uploaded images using the following endpoint

```bash
GET /api/v1/images
```

This will return a list of all the user's uploaded images, including the file name and thumbnail links of a different sizes based on the user's account plan.

## Uploading an Image

Users can upload an image using the following endpoint

```bash
POST /api/v1/images
```

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



