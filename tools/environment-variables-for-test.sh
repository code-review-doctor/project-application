export SKIP_S3_TESTS=1
export FORCE_SQLITE3_DATABASE=1

export OBJECT_STORAGE_SECRET_ACCESS_KEY=not_needed_for_tests
export OBJECT_STORAGE_BUCKET_NAME=projects
export OBJECT_STORAGE_PREFIX_LOCATION=projects
export FROM_EMAIL=notification@example.com
export EMAIL_HOST=smtp.example.com
export EMAIL_HOST_USER=john@example.com
export EMAIL_HOST_PASSWORD=this_is_not_the_password
export EMAIL_SUBJECT_PREFIX=[ProjectsApplicationUnitTest]
export ADMIN_1=Name,name@example.com
export DEBUG=1
export ALLOWED_HOST_1=127.0.0.1
export OBJECT_STORAGE_ACCESS_KEY_ID=key
export OBJECT_STORAGE_ENDPOINT_URL=http://localhost:9000
