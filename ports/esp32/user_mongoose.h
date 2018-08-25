
#define BitHostName "bit.bpi"

#define MG_PORT_HTTP "80"
#define MG_PORT_DNS "udp://:53"

bool mg_start();

void mg_close();

void mg_poll();

