https://github.com/benborla/mcp-server-mysql
安装：
npm install -g @benborla29/mcp-server-mysql
让calude执行并修改 claude.json

claude mcp add mcp_server_mysql \
  -e MYSQL_HOST="127.0.0.1" \
  -e MYSQL_PORT="3306" \
  -e MYSQL_USER="root" \
  -e MYSQL_PASS="1" \
  -e MYSQL_DB="1" \
  -e ALLOW_INSERT_OPERATION="true" \
  -e ALLOW_UPDATE_OPERATION="true" \
  -e ALLOW_DELETE_OPERATION="false" \
  -- npx @benborla29/mcp-server-mysql
