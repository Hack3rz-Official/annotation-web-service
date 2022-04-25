set -e

# TODO: add indices on collections?
# will only be executed if there is no ./data:/data/db
mongo <<EOF
use admin

db.createUser({
    user: '$MONGO_USERNAME',
    pwd:  '$MONGO_PASSWORD',
    roles: [{
        role: 'readWrite',
        db: '$MONGO_DATABASE_NAME'
    }, {
        role: 'readWrite',
        db: '$MONGO_DATABASE_TEST_NAME'
    }]
})
EOF