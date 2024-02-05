#!/bin/sh
echo "
window.env = {
BACKEND_URL: '$BACKEND_URL',
PROJECT: '$PROJECT',
};
" > /usr/share/nginx/html/env-config.js

# Start Nginx
nginx -g "daemon off;"