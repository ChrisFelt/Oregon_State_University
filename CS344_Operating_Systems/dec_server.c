// Title: dec_server
// Author: Christopher Felt
// Class: CS 344 OS1
// Description: Server daemon that receives TCP connections only from dec_client. Creates a 
//              new child with fork each time dec_client connects. Child receives ciphertext 
//              and key from client, decrypts ciphertext using the one-time pad method, and 
//              sends the resulting plaintext file to the client.
// Sources: dec_server starter code, https://beej.us/guide/bgnet/html/#a-simple-stream-server,
//          https://beej.us/guide/bgnet/html/#sendall, and lots of man pages

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
// include ctype.h for isupper() function
#include <ctype.h>
#include <stdbool.h>
#include <errno.h>

// authentication message and end of message syntax
#define AUTHENTICATE "decode"
#define EOM "@@"
#define EOM_CHAR '@'

#define BACKLOG 10   // how many pending connections queue will hold

// server communicates with 256 byte long messages
#define MSG_BUFFER_SIZE 256
// potentially need a LOT of space for the plaintext/cipher messages
// this will also serve as the key buffer size
#define TEXT_BUFFER_SIZE 96000

// array of the 27 allowed characters
static char const allowed_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ";

static volatile sig_atomic_t num_children = 0;


// --------------------------------------------------------------------
// SIGNAL HANDLING
// --------------------------------------------------------------------

// Handler for SIGCHLD
// Source: https://beej.us/guide/bgnet/html/#a-simple-stream-server
void handle_SIGCHLD(int signo) {  

  // save errno since waitpid can overwrite it
  int prev_errno = errno;

  // clean up any child processes that have terminated
  // on success, waitpid returns the pid of the child, otherwise it returns 0 (or -1 if it fails)
  // if we pass -1 instead of a child pid, it will wait for any child process
  // we are not interested in HOW the child terminated, so no need to bother with status 
  while (waitpid(-1, NULL, WNOHANG) > 0) {
    // decrement the number of child processes active
    --num_children;
    //write(STDOUT_FILENO, "Zombie child removed\n", 21); // debug
  }

  // restore errno
  errno = prev_errno;

} // end handle_SIGCHLD


// --------------------------------------------------------------------
// FUNCTION DECLARATIONS
// --------------------------------------------------------------------

// name: is_allowed
// purpose: check if a buffer contains characters besides the 27 allowed
// input: the char array to check and its length
// output: bool: true if all chars allowed, otherwise false
int is_allowed(char *array, int length);


// name: append_eom
// purpose: append EOM to a string to signify the end of the message
// input: char array to append EOM to
// output: none, appends in place
// WARNING: does not check for buffer overflow!
void append_eom(char *array);


// name: decrypt
// purpose: decrypt plaintext using the one-time pad method with a key
// input: plaintext, key, and ciphertext char arrays, and their length
// output: none, writes decrypted text in place to ciphertext buffer
void decrypt(char *plaintext, char *keytext, char *ciphertext, int length);


// name: error
// purpose: error function used for reporting issues
// input: error message
// output: none, ENDS EXECUTION WITH EXIT STATUS 1
void error(const char *msg);


// name: copy_buf_from_pos
// purpose: copies (in place) a buffer from a given index to the null terminator
// input: the buffer to copy, index position to start from, and the buffer length
// output: none, original buffer is cleared and replaced with the new contents
void copy_buf_from_pos(char *copy_buffer, int pos, int length);


// name: recv_msg
// purpose: copy received messages from the socket until end of message marker received
// input: socket file descriptor, the destination buffer, a buffer to store post-EOM message,
//        and the lengths of the two buffers
// output: 0 on success; full message will be copied in place to the destination buffer. 
//         -1 on failure
int recv_msg(int socket_fd, char *fulltext_buffer, char *store_msg, 
             int ft_buf_len, int store_msg_len);


// name: send_msg
// purpose: send all until until full message sent
// input: socket file descriptor, buffer containing message
// output: 0 on success, -1 on failure
// SOURCE: https://beej.us/guide/bgnet/html/#sendall
int send_msg(int socket_fd, char *buffer);


// name: get_in_addr
// purpose: get sockaddr for either IPv4 or IPv6
// input: sockaddr struct pointer
// output: none 
void *get_in_addr(struct sockaddr *sa);


// --------------------------------------------------------------------
// MAIN
// --------------------------------------------------------------------

int main(int argc, char *argv[]) {
  // initialize network variables
  int sock_fd, new_fd;  // listen on sock_fd, new connection on new_fd
  struct addrinfo hints, *servinfo, *p;
  struct sockaddr_storage their_addr; // connector's address information
  socklen_t sin_size;
  struct sigaction sa;
  int yes = 1;
  char s[INET6_ADDRSTRLEN];
  int rv;

  // general use and authenticate buffers
  char buffer[MSG_BUFFER_SIZE];
  char authenticate[MSG_BUFFER_SIZE];
  char store_msg[MSG_BUFFER_SIZE];

  // initialize number of currently active children
  pid_t spawnpid; // holds forked child pid

  // initialize the encrypted text, plaintext, and key character buffers
  char ciphertext[TEXT_BUFFER_SIZE];
  char plaintext[TEXT_BUFFER_SIZE];
  char keytext[TEXT_BUFFER_SIZE];

  // Check usage & args
  if (argc < 2) { 
    fprintf(stderr,"USAGE: %s port\n", argv[0]); 
    exit(1);
  } 


  // --------------------------------------------------------------------
  // REGISTER SIGNAL HANDLER
  // --------------------------------------------------------------------
  // setup signal handler for cleaning up terminated child processes
  // NOTE: alternatively, we could explicitly set the handler for SIGCHLD to SIG_IGN
  // this would immediately remove terminated child processes... sounds much easier
  struct sigaction SIGCHLD_action = {0};

  // register a handler for SIGCHLD signal
  SIGCHLD_action.sa_handler = handle_SIGCHLD;
  // ignore other signals until the signal handler is done
  sigfillset(&SIGCHLD_action.sa_mask);
  SIGCHLD_action.sa_flags = SA_RESTART; // no flags
  
  // register the handler - sigaction returns 0 on success and -1 on error
  if (sigaction(SIGCHLD, &SIGCHLD_action, NULL) == -1) {
    error("dec_server: SIGCHLD handler registration failed!");
  }
  

  // --------------------------------------------------------------------
  // SOCKET CREATION
  // --------------------------------------------------------------------
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE; // use my IP

  // call getaddrinfo with port info to fill in structs
  // node is NULL and AI_PASSIVE is set for hints_ai.flags, so server will accept
  // connections on any of the host's network addresses (according to man getaddrinfo)
  if ((rv = getaddrinfo(NULL, argv[1], &hints, &servinfo)) != 0) {
    fprintf(stderr, "dec_server: getaddrinfo: %s\n", gai_strerror(rv));
    return 1;
  }

  // loop through all the results and bind to the first we can
  for(p = servinfo; p != NULL; p = p->ai_next) {
    // go to next result if socket() fails
    if ((sock_fd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
      continue;
    }

    // exit with errors if setsockopt() fails
    if (setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
      error("dec_server: setsockopt");
    }

    // go to next result if bind() fails
    if (bind(sock_fd, p->ai_addr, p->ai_addrlen) == -1) {
      close(sock_fd); // close the socket fd we opened earlier
      continue;
    }

    break; // no errors!
  }

  freeaddrinfo(servinfo); // all done with this structure

  if (p == NULL)  {
    fprintf(stderr, "dec_server: failed to bind\n");
    exit(1);
  }

  if (listen(sock_fd, BACKLOG) == -1) {
    error("dec_server: listen");
  }
  

  // --------------------------------------------------------------------
  // ACCEPT CONNECTIONS AND SPAWN CHILDREN
  // --------------------------------------------------------------------
  // Accept a connection, blocking if one is not available until one connects
  while(1){

    // don't attempt to accept new connections if 5 children are currently active
    if (num_children == 5) {
      continue;
    }

    // Accept the connection request which creates a connection socket
    sin_size = sizeof their_addr;
    new_fd = accept(sock_fd, (struct sockaddr *)&their_addr, &sin_size);
    if (new_fd == -1) {
      perror("dec_server: accept");
      continue; // try accept again
    }

    inet_ntop(their_addr.ss_family, get_in_addr((struct sockaddr *)&their_addr), s, sizeof s);

    // now that we're connected, we spawn a child to handle the connection
    spawnpid = -5;
    // fork new child
    spawnpid = fork();
    switch(spawnpid) {
      // just skip if fork fails
      case -1: 
        perror("dec_server: fork() failed");
        continue;
      

      // --------------------------------------------------------------------
      // CHILD
      // --------------------------------------------------------------------
      // if this is the child, spawnpid = 0
      case 0:

        // close listening socket since we don't need it in the child
        close(sock_fd);

        // --------------------------------------------------------------------
        // AUTHENTICATE CONNECTION
        // --------------------------------------------------------------------
        // clear stored messages for first call of recv_msg
        memset(store_msg, '\0', sizeof(store_msg));
        // dec_client will always send "decode@@" as its first message
        // Get the message from the client and display it
        if (recv_msg(new_fd, authenticate, store_msg, 
                     MSG_BUFFER_SIZE, MSG_BUFFER_SIZE) == -1) {
          close(new_fd);
          error("dec_server: ERROR reading AUTHENTICATE from socket");
        }
        //printf("dec_server: Received %s\n", authenticate);

        // send decode@@ back to the client to establish connection
        memset(buffer, '\0', sizeof(buffer));
        strcpy(buffer, AUTHENTICATE);
        append_eom(buffer);
        if (send_msg(new_fd, buffer) == -1) { // error check
          close(new_fd);
          error("dec_server: ERROR writing AUTHENTICATE to socket");
        }
        
        // close connection if the client is not dec_client
        if (strcmp(authenticate, AUTHENTICATE) != 0) {
          fprintf(stderr, "dec_server: Child could not authenticate and will exit.\n");
          close(new_fd);
          exit(1);
        }


        // --------------------------------------------------------------------
        // RECEIVE CIPHERTEXT
        // --------------------------------------------------------------------
        // server receives ciphertext 
        if (recv_msg(new_fd, ciphertext, store_msg, 
                     TEXT_BUFFER_SIZE, MSG_BUFFER_SIZE) == -1) {
          close(new_fd);
          error("dec_server: ERROR reading CIPHERTEXT from socket");
        }
        //printf("dec_server: Ciphertext received: \"%s\"\n", ciphertext);

        // exit with errors if ciphertext contains non-allowed chars
        if (!is_allowed(ciphertext, TEXT_BUFFER_SIZE)) {
          fprintf(stderr, "dec_server: CIPHERTEXT contains non-allowed characters.\n");
          close(new_fd);
          exit(1);
        }


        // --------------------------------------------------------------------
        // RECEIVE KEY
        // --------------------------------------------------------------------
        // server receives key
        if (recv_msg(new_fd, keytext, store_msg, 
                     TEXT_BUFFER_SIZE, MSG_BUFFER_SIZE) == -1) {
          close(new_fd);
          error("dec_server: ERROR reading KEY from socket");
        }
        //printf("dec_server: Key received: \"%.*s\"\n", 1921, keytext);

        // exit with errors if keytext contains non-allowed chars
        if (!is_allowed(keytext, TEXT_BUFFER_SIZE)) {
          fprintf(stderr, "dec_server: KEY contains non-allowed characters.\n");
          close(new_fd);
          exit(1);
        }

        // exit with errors if ciphertext is longer than keytext
        if (strlen(ciphertext) > strlen(keytext)) {
          fprintf(stderr, "dec_server: KEY does not contain enough characters.\n");
          close(new_fd);
          exit(1);
        }


        // --------------------------------------------------------------------
        // SEND PLAINTEXT AND CLOSE CONNECTION
        // --------------------------------------------------------------------
        // server decrypts the ciphertext using keytext
        decrypt(plaintext, keytext, ciphertext, TEXT_BUFFER_SIZE);

        // server sends decrypted text
        // append end of message '@@' first
        append_eom(plaintext);
        if (send_msg(new_fd, plaintext) == -1) {
          close(new_fd);
          error("dec_server: ERROR writing PLAINTEXT to socket");
        }
        //printf("dec_server: Sent %s\n", plaintext);

        // child closes the connection for this socket and exits
        close(new_fd);
        exit(0); 


      // --------------------------------------------------------------------
      // PARENT - SERVER DAEMON
      // --------------------------------------------------------------------
      // in the parent process
      default:
        // increment child count
        ++num_children;

    } 
  }

  // we will never reach this point but...
  // Close the listening socket
  close(sock_fd); 
  return 0;
} // end main


// --------------------------------------------------------------------
// FUNCTION DEFINITIONS
// --------------------------------------------------------------------

// is_allowed
int 
is_allowed(char *array, int length) {
  int i;

  // iterate through the char array
  for (i = 0; i < length; ++i) {
    
    // exit loop if we reach null terminator
    if (array[i] == '\0') {
      break;
    }

    // if the current index is not an uppercase letter or space, return false
    // isupper() returns nonzero (true) if the character is not uppercase 
    if (array[i] != ' ' && !isupper(array[i])) {
      return false;
    }
  }

  // buffer contains allowed chars
  return true;
} // end is_allowed


// append_eom
void 
append_eom(char *array) {
  // append EOM to end of string
  array[strlen(array)] = EOM_CHAR;
  array[strlen(array)] = EOM_CHAR;
}


// decrypt ciphertext
void 
decrypt(char *plaintext, char *keytext, char *ciphertext, int length) {
  int i;
  int cur_ciphertext; // holds converted decimal value of the current ciphertext character
  int cur_keytext; // holds converted decimal value of the current keytext character
  int cur_plaintext; // decrypted text

  // to get plaintext[i], we will subtract the keytext[i] from ciphertext[i]
  // for  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z  ' '
  // sub  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26

  // iterate through the buffers
  for (i = 0; i < length; ++i) {
    
    // once we reach the end of ciphertext, we're done decrypting the message
    if (ciphertext[i] == '\0') {
      break;
    }

    // GET CONVERTED VALUE OF CIPHERTEXT
    // check if ciphertext[i] is a space
    if (ciphertext[i] == ' ') {
      // our value of ciphertext from above is 26, so
      cur_ciphertext = 26;
    }
    else {
      // ASCII decimal value of A is 65, so we subtract that from the ASCII value of 
      // ciphertext[i] in order to get our value of ciphertext
      cur_ciphertext = (int)ciphertext[i];
      cur_ciphertext = cur_ciphertext - 65;
    }

    // now we repeat with keytext
    // GET CONVERTED VALUE OF KEYTEXT
    // check if keytext[i] is a space
    if (keytext[i] == ' ') {
      // our value of keytext from above is 26, so
      cur_keytext = 26;
    }
    else {
      // ASCII decimal value of A is 65, so we subtract that from the ASCII value of 
      // keytext[i] in order to get our value of keytext
      cur_keytext = (int)keytext[i];
      cur_keytext = cur_keytext - 65;
    }

    // unlike with encryption, we can get negative numbers decrypting
    // so we need to add 27 if the result is negative in order to get the correct value
    cur_plaintext = cur_ciphertext - cur_keytext;
    if (cur_plaintext < 0) {
        cur_plaintext = cur_plaintext + 27;
    }

    // finally, we add the converted values modulo 27 to get the appropriate character
    // from the allowed_chars array, which gives us our decrypted character
    plaintext[i] = allowed_chars[cur_plaintext % 27];

  }

} // end decrypt


// error
void 
error(const char *msg) {
  perror(msg);
  exit(1);
} 


// copy_buf_from_pos
void 
copy_buf_from_pos(char *copy_buffer, int pos, int length) {
    
    int i;
    // declare and clear temp buffer
    char temp[length];
    memset(temp, '\0', sizeof(temp));


    // copy dest to temp buffer starting at 
    for (i = 0; i < length; ++i) {
        temp[i] = copy_buffer[pos + i];
    }

    // clear copy buffer
    memset(copy_buffer, '\0', sizeof(copy_buffer));
    // copy contents of temp to copy buffer
    strcpy(copy_buffer, temp);    

} // end copy_buf_from_pos


// recv_msg
int 
recv_msg(int socket_fd, char *fulltext_buffer, char *store_msg, 
         int ft_buf_len, int store_msg_len) {
  
  // temp buffer to hold partial received message 
  char msg_buffer[store_msg_len];
  // get size of fulltext buffer to avoid buffer overflow
  int i;
  int j = 0; // track destination buffer index
  int chars_read;
  
  // clear destination buffer and msg buffer
  memset(fulltext_buffer, '\0', sizeof(fulltext_buffer));
  memset(msg_buffer, '\0', sizeof(msg_buffer));

  // copy remaining chars from previous receive
  if (store_msg[0] != '\0') {

    // iterate through the stored message buffer
    for (i = 0; i < store_msg_len; ++i) {
      
      // stop copying if we reacha  null terminator in the stored message buffer
      if (store_msg[i] == '\0') {
        break;
      }
      
      // copy current index of stored message to the full message and increment the
      // full message index
      fulltext_buffer[j] = store_msg[i];
      ++j;  

      // check for EOM if we are not at i = 0
      if (i > 0) {  
        // check if fulltext contains EOM
        if (fulltext_buffer[i] == EOM_CHAR && fulltext_buffer[i - 1] == EOM_CHAR) {
          // clear EOM
          fulltext_buffer[i] = '\0';
          fulltext_buffer[i - 1] = '\0';
          
          // save remaining stored buffer
          copy_buf_from_pos(store_msg, i + 1, store_msg_len);  

          return 0; // return successful receipt of message
        }
      }    

    } // end for loop

    // all of the contents of stored buffer have been copied if we reach this point
    // clear the stored message buffer for reuse
    memset(store_msg, '\0', sizeof(store_msg));
  }
        
  // Read the client's message from the socket until end of message ("@@") is received 
  while (j < ft_buf_len) {
    memset(msg_buffer, '\0', sizeof(msg_buffer));
    // receive message and check for errors
    chars_read = recv(socket_fd, msg_buffer, store_msg_len - 1, 0);
    
    if (chars_read < 0) {
      return -1;
    }

    // copy to destination buffer
    for (i = 0; i < chars_read + 1; ++i) {

      if (msg_buffer[i] == '\0') {
        break;
      }

      // write current buffer index to current destination buffer index
      fulltext_buffer[j] = msg_buffer[i];
      
      // break loop when end of message is reached
      // don't copy @ symbols to destination buffer
      // max chars_read will always be msg_buf_len - 1, so we can look at the next char
      if (j > 0) {

        if (fulltext_buffer[j] == EOM_CHAR && fulltext_buffer[j - 1] == EOM_CHAR) {
          // clear EOM
          fulltext_buffer[j] = '\0';
          fulltext_buffer[j - 1] = '\0';
          
          // store the rest of the message, if any
          if (msg_buffer[i + 1] != '\0') {
            
            // copy full message to store buffer then copy from pos
            strcpy(store_msg, msg_buffer);
            copy_buf_from_pos(store_msg, i + 1, store_msg_len);  

          }

          return 0; // return successful receipt of message
        }

      } // end check for EOM

      ++j; // increment destination buffer index counter
    } // end copy msg to dest

  } // end get full message

  return 0; // success!

} // end of recv_msg


// send_msg
int 
send_msg(int socket_fd, char *buffer) {

  // track current number of chars that need to be sent
  int chars_left = strlen(buffer);
  // track the total number of chars sent
  int chars_sent = 0;
  // track the chars sent in the current send call
  int chars_written;

  // send chars until everything is sent
  while (chars_sent < chars_left) {

    // current send call attempts to send the remaining chars
    // index through the send buffer by using the total number of chars sent  
    // to pick up where we left off from the previous send (if applicable) 
    chars_written = send(socket_fd, buffer + chars_sent, chars_left, 0);

    // check for errors
    if (chars_written == -1) {
      break;
    }

    // adjust total number of chars sent and chars remaining by the 
    // chars that were sent this pass
    chars_sent += chars_written;
    chars_left -= chars_written;

  }

  // use a ternary expression to check if there was an error above
  // if error return -1, else return 0
  return chars_written == -1 ? -1 : 0;

} // end of send_msg


// name: get_in_addr
void *get_in_addr(struct sockaddr *sa)
{
  if (sa->sa_family == AF_INET) {
    return &(((struct sockaddr_in*)sa)->sin_addr);
  }

  return &(((struct sockaddr_in6*)sa)->sin6_addr);

} // end of get_in_addr
