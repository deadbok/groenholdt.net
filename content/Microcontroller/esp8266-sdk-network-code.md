author: ObliVion
date: 2015-08-24 22:00
tags: esp8266, esp12, Microcontroller, c
title: ESP8266 network code.
type: post
template: post

Since I began programming the ESP8266, I have been struggling to
get the TCP network API of the SDK working consistently without
crashes. I think that I have cracked it at last. Here are some
notes, so that I may never forget, and maybe help someone else.

ESP8266 TCP server.
===================

This post is about using the ESP8266 as TCP server, but the information
is useful if you want to know how to tackle ESP8266 networking in
general. First lets set up a server like the SDK tells us to do it:

 * Initialise struct espconn parameters according the protocol type you
   want (``ESPCONN_TCP``).
 * Register connect callback and reconnect callback functions.
 * Call ``espconn_accept`` to start listening for packets.
 * When a connection has been made on the listening connection, the
   registered connect callback is called.
   
Some code to do this:

	bool ICACHE_FLASH_ATTR tcp_listen(unsigned int port)
	{
		int ret;
		struct espconn *conn;
		
		//Get some memory for the connection information.
		conn = os_zalloc(sizeof(struct espconn));
		if (conn)
		{
			//Set up TCP connection configuration.
			//TCP connection.
			conn->type = ESPCONN_TCP;
			//No state.
			conn->state = ESPCONN_NONE;
			//Set port.
			conn->proto.tcp->local_port = port;

			//Register SDK callbacks.
			espconn_regist_connectcb(conn, tcp_connect_cb);
			espconn_regist_reconcb(conn, tcp_reconnect_cb);
			espconn_regist_disconcb(conn, tcp_disconnect_cb);
				
			ret = espconn_accept(conn);
			if (ret != ESPCONN_OK)
			{
				os_printf("Error when starting the listener: %d.\n", ret);
				return(false);
			}
			return(true);
		}
		os_printf("Could not allocate memory for the listening connection.\n");
		return(false);
	}

Callbacks.
==========

The SDK network API is event based. The way this works is that you
register some functions for the API to call when certain events happen 
(connected, disconnected, data received, and so on).
Your callback function receives a parameter called ``arg``, from the SDK,
which is a pointer to an espconn struct (defined in espconn.h in the
SDK). This struct contains the connection information. You will probably
need a way to identify a connection as it triggers the callbacks. I have 
additional data from my own application coupled to the connection, 
that I need to handle when an event happens to the connection. In fact I
have a list of all open connections using my own data structures. When I
first started using the ESP8266 I ignored the part of the *Programming
Guide*, that told me to not use the ``arg`` pointer from the callbacks,
to distinguish one connection from another.
The following is an example of a struct I was using at the time to keep
track of connections.

	struct tcp_connection
	{
		//Pointer to the struct espconn structure associated with the
		//connection.
		struct espconn *conn;
		//Pointer to the data meant for the current callback.
		struct tcp_callback_data callback_data;
		//Is the connection sending data.
		bool sending;
		//Are the connection closing.
		bool closing;
		//A pointer for the user, never touched.
		void *user;
		//Pointers for the prev and next entry in the list.
		struct tcp_connection *prev;
		struct tcp_connection *next;
	};

When ever the program entered a callback, the code would compare the
``arg`` pointer to the one stored in the ``conn`` member of 
``tcp_connection``, and couple my private data to the connection that
way. This works most of the time, but fails in couple if cases. 

 1. *The SDK tells us not to do this, which in my book tells me,
	that sometime later the SDK may change internally enough, that this
	could stop working.*
 2. The reconnect and disconnect callbacks gets an ``arg`` parameter
    passed, that point to the listening connection, not the one that the
    event happened too.

There are ways around the second problem that works quite well, but
why bother when the whole thing may break with some later version of the
SDK, and there is a nicer option outlined in the *Programming Guide*?

The solution from the *Programming Guide* is to use the remote address 
and port to identify each connection. This took a little more code, but
when done, revealed a few things about the flow of the connections in
the API.

Connection flow in the ESP8266 API.
===================================

Let us look at some excerpts of debug log files from my HTTP server:

Listening connection.
---------------------

Just after the ``espconn_accept`` call the situation looks like this:

	Connection 0x3fff3158 (0x3fff3480) state "ESPCONN_LISTEN".
	 Remote address 0.0.0.0:0.
	 SDK remote address 0.0.0.0:0.
	1 connection.
	
This is the listening connection. **This connection is the one that the
remote computer connects to, and has to remain open as long as the
server is expected to serve connections.** ``0x3fff3480`` is a pointer to
the struct espconn data for the connection. ``0x3fff3158`` is the
connection data, that I am keeping. The struct looks somewhat like this:

	struct tcp_connection
	{
		//SDK connection data.
		struct espconn *conn;
		//Remote IP.
		uint8 remote_ip[4];
		//Remote port.
		unsigned int remote_port;
		//Local IP.
		uint8 local_ip[4];
		//Remote port.
		unsigned int local_port;
		//Pointer to the data meant for the current callback.
		struct tcp_callback_data callback_data;
		//Pointers to callback functions for handling connection states.
		struct tcp_callback_funcs *callbacks;
		//Is the connection sending data.
		bool sending;
		//Is the connection closing.
		bool closing;
		//Pointers for the prev and next entry in the list.
		struct tcp_connection *prev;
		struct tcp_connection *next;
	};

As will later become clear, ``espconn`` may be deallocated by the SDK.
Any data that you may need to preserve to keep track of the connection
should be copied somewhere else, hence the IP addresses and ports in the
above struct.

New connection.
---------------

Next up someone is connecting to the server:

	TCP connected (0x3fff3cb8).
	Connection 0x3fff3158 (0x3fff3480) state "ESPCONN_CONNECT".
	 Remote address 0.0.0.0:0.
	 SDK remote address 192.168.4.2:34480.
	1 connection.
	
``0x3fff3cb8`` is the address of a new ``espconn`` struct, that the SDK
has created for the incoming connection. This is where I create a new
``tcp_connection`` struct, and add it to the list of connections. The 
``Remote address`` is the one saved when the connection was created, and
the ``SDK remote address`` is the one currently in the ``espconn``
struct.

Data received.
--------------

A request comes in:

	TCP received (0x3fff3cb8).
	Connection 0x3fff3158 (0x3fff3480) state "ESPCONN_CONNECT".
	 Remote address 0.0.0.0:0.
	 SDK remote address 192.168.4.2:34480.
	Connection 0x3fff3d18 (0x3fff3cb8) state "ESPCONN_READ".
	 Remote address 192.168.4.2:34480.
	 SDK remote address 192.168.4.2:34480.
	2 connections.

The callback gets a pointer to the newly created ``espconn`` struct, but
still according to the docs we can not expect this behaviour.

Sending the answer.
-------------------

To answer the request, find the connection that has a remote address 
of 192.168.4.2:34480 and use the ``espconn`` pointer (0x3fff3cb8) 
when calling ``espconn_send``. After calling ``espconn_send`` you have
to wait for the sent callback before sending any more data. I have not
seen any mention of the data size limit of ``espconn_send`` in the
official docs, but I have seen 1440 bytes mentioned elsewhere. You may
have to split your data and do more than one ``espconn_send``, wait,
sent callback cycle.

This is what the situation looks like when entering the sent callback:

	TCP sent (0x3fff3cb8).
	Connection 0x3fff3158 (0x3fff3480) state "ESPCONN_CONNECT".
	 Remote address 0.0.0.0:0.
	 SDK remote address 192.168.4.2:34480.
	Connection 0x3fff3d18 (0x3fff3cb8) state "ESPCONN_CONNECT".
	 Remote address 192.168.4.2:34480.
	 SDK remote address 192.168.4.2:34480.
	2 connections.
	
This is where the penny finally dropped for me. Notice the SDK remote
addresses? It may be obvious, but the listening connection tracks the
state of the currently sending connection. It looks like listening
connection does the actual sending.

Closing the connection.
-----------------------

What happens when the connection is closing, or an error (reconnect)
occurs, makes sense after seeing the above, but eluded me for a long
time.

	TCP disconnected (0x3fff3480).
	Connection 0x3fff3158 (0x3fff3480) state "ESPCONN_CLOSE".
	 Remote address 0.0.0.0:0.
	Connection 0x3fff3d18 (0x3fff3cb8) state "ESPCONN_CLOSE".
	 Remote address 192.168.4.2:34480.
	2 connections.

The SDK is a harsh mistress, and deallocates the ``espconn`` connection
data before calling the disconnect/reconnect callback. That is why
there is no SDK remote addresses and also why I saved the remote
address in my own connection data earlier. The ``espconn`` pointer 
returned in the ``arg`` parameter of the callback still contain the
remote address of the closing connection (and points to the listening
connection). The code uses this to look up the connection and deallocate
my stuff.
