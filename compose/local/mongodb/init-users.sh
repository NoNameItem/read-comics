if [ "$MONGODB_ROOT_USER" ] && [ "$MONGODB_ROOT_PASSWORD" ]; then
  "${mongo[@]}" "$MONGODB_DATABASE" <<-EOJS
  db.createUser({
     user: $(_js_escape "$MONGODB_ROOT_USER"),
     pwd: $(_js_escape "$MONGODB_ROOT_PASSWORD"),
     roles: [ "readWrite", "dbAdmin" ]
     })
EOJS
fi

echo ======================================================
echo created $MONGODB_ROOT_USER in database $MONGODB_DATABASE
echo ======================================================
