// Title: enc_client
// Author: Christopher Felt
// Class: CS 344 OS1
// Description: Client that connects to only enc_server via TCP. Reads the contents of
//              the given plaintext and key files, sends them to the server, receives the
//              encrypted text from the server, and outputs to stdout with appended newline 
//              char.
// Sources: enc_client starter code, https://beej.us/guide/bgnet/html/#a-simple-stream-client, 
//          https://beej.us/guide/bgnet/html/#sendall, and some man pages

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>  // ssize_t
#include <sys/socket.h> // send(),recv()
#include <netdb.h>      // gethostbyname()
#include <ctype.h>
#include <stdbool.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define HOST "localhost"
// authentication message and end of message syntax
#define AUTHENTICATE "encode"
#define EOM "@@"
#define EOM_CHAR '@'

// client communicates with 256 byte long messages
#define MSG_BUFFER_SIZE 256
// potentially need a LOT of space for the plaintext/cipher messages
// this will also serve as the key buffer size
#define TEXT_BUFFER_SIZE 96000


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
  int socket_fd, numbytes;  
  struct addrinfo hints, *servinfo, *p;
  int rv;
  char s[INET6_ADDRSTRLEN];

  // initialize general variables
  char buffer[MSG_BUFFER_SIZE];
  char store_msg[MSG_BUFFER_SIZE];
  memset(buffer, '\0', sizeof(buffer));
  memset(store_msg, '\0', sizeof(store_msg));

  // Check usage & args TODO: check if too many args used?
  if (argc < 4) { 
    fprintf(stderr,"USAGE: %s plaintext key port\n", argv[0]); 
    exit(1); 
  } 

  // get the port number argument
  char *port_num = argv[3];


  // --------------------------------------------------------------------
  // READ FILE INPUT TO BUFFERS
  // --------------------------------------------------------------------
  // initialize file variables
  FILE *plaintext_file;
  FILE *keytext_file;

  // open plaintext file
  plaintext_file = fopen(argv[1], "r");
  // check for errors
  if (plaintext_file == NULL) {
    error("Error opening plaintext");
  }

  // open key file
  keytext_file = fopen(argv[2], "r");
  // check for errors
  if (keytext_file == NULL) {
    fclose(plaintext_file);
    error("Error opening key");
  }

  // initialize buffers to hold file contents and encrypted result
  char plaintext[TEXT_BUFFER_SIZE];
  char keytext[TEXT_BUFFER_SIZE];
  char ciphertext[TEXT_BUFFER_SIZE];

  // zero out the buffers
  memset(plaintext, '\0', sizeof(plaintext));
  memset(keytext, '\0', sizeof(keytext));
  memset(ciphertext, '\0', sizeof(ciphertext));

  // save contents of files to buffers with fgets
  // first, read plaintext file
  if (fgets(plaintext, TEXT_BUFFER_SIZE, plaintext_file) == NULL) {
    fprintf(stderr, "enc_client: fgets PLAINTEXT failed.\n");
    exit(1);
  }
  // the file must end in a newline, so we strip the last character from plaintext
  plaintext[strlen(plaintext) - 1] = '\0';

  // close plaintext file
  if (fclose(plaintext_file) != 0) {
    error("enc_client: Error closing PLAINTEXT");
  } 

  // next, read key file and check for errors
  if (fgets(keytext, TEXT_BUFFER_SIZE, keytext_file) == NULL) {
    fprintf(stderr, "enc_client: fgets KEYTEXT failed.\n");
    exit(1);
  }
  // the file must end in a newline, so we strip the last character from keytext
  keytext[strlen(keytext) - 1] = '\0';

  // close keytext file
  if (fclose(keytext_file) != 0) {
    error("enc_client: Error closing KEYTEXT");
  }

  // check that plaintext contains ONLY allowed characters
  if (!is_allowed(plaintext, TEXT_BUFFER_SIZE)) {
    // exit with errors
    fprintf(stderr, "enc_client: PLAINTEXT contains non-allowed characters.\n");
    exit(1);
  }

  // check that plaintext contains ONLY allowed characters
  if (!is_allowed(keytext, TEXT_BUFFER_SIZE)) {
    // exit with errors
    fprintf(stderr, "enc_client: KEYTEXT contains non-allowed characters.\n");
    exit(1);
  }

  // check that keytext is at least as long as plaintext
  if (strlen(plaintext) > strlen(keytext)) {
    // exit with errors
    fprintf(stderr, "enc_client: KEYTEXT is shorter than PLAINTEXT!\n");
    exit(1);
  }

  // append '@@' to the end of the strings to signify end of message for the server
  append_eom(plaintext);
  append_eom(keytext);


  // --------------------------------------------------------------------
  // CONNECT TO SERVER
  // --------------------------------------------------------------------
  // now that we know there are no file errors, connect to the server
  // zero out hints struct and fill it in
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;

  // call getaddrinfo with host and port info to fill in structs
  if ((rv = getaddrinfo(HOST, argv[3], &hints, &servinfo)) != 0) {
    fprintf(stderr, 
      "enc_client: Failed to connect to server on port %s! getaddrinfo: %s\n", 
      port_num, gai_strerror(rv));
    return 2;
  }

  // loop through all the results and connect to the first we can
  for(p = servinfo; p != NULL; p = p->ai_next) {
    // try to open the socket fd
    // if it fails, try the next result
    if ((socket_fd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
      continue;
    }

    // try to connect
    if (connect(socket_fd, p->ai_addr, p->ai_addrlen) == 0) {
      break; // success!
    }

    // if connect failed, close the socket fd and try the next result
    close(socket_fd);
  }

  if (p == NULL) {
    fprintf(stderr, "enc_client: Failed to connect to server on port %s!\n", port_num);
    return 2;
  }

  inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr), s, sizeof s);

  freeaddrinfo(servinfo); // all done with this structure


  // --------------------------------------------------------------------
  // AUTHENTICATE
  // --------------------------------------------------------------------
  // Send authentication message to server
  // first, copy authentication message to buffer
  memset(buffer, '\0', sizeof(buffer));
  strcpy(buffer, AUTHENTICATE);
  append_eom(buffer); // append end of message marker
  // send message to server
  if (send_msg(socket_fd, buffer) == -1) {
    error("enc_client: ERROR writing AUTHENTICATE to socket");
  }
  //printf("enc_client: Sent %s\n", buffer);

  // Receive authentication message from server
  if (recv_msg(socket_fd, buffer, store_msg, MSG_BUFFER_SIZE, MSG_BUFFER_SIZE) == -1) {
    error("enc_client: ERROR reading from socket");
  }
  //printf("enc_client: Received %s\n", buffer);

  // if connection is not to enc_server, exit with error code 2
  if (strcmp(buffer, AUTHENTICATE) != 0) {
    fprintf(stderr, "enc_client: Could not connect to server on port %s!\n", port_num);
    exit(2);
  }


  // --------------------------------------------------------------------
  // SEND PLAINTEXT
  // --------------------------------------------------------------------
  // Send plaintext to server
  // plaintext buffer is ready to go, so we will send it as is
  if (send_msg(socket_fd, plaintext) == -1) {
    error("enc_client: ERROR writing PLAINTEXT to socket");
  }
  //printf("enc_client: Sent %s\n", plaintext);


  // --------------------------------------------------------------------
  // SEND KEYTEXT
  // --------------------------------------------------------------------
  // Send keytext to server
  // keytext buffer is also ready to go, so we will send it as is
  if (send_msg(socket_fd, keytext) == -1) {
    error("enc_client: ERROR writing PLAINTEXT to socket");
  }
  //printf("enc_client: Sent %s\n", keytext);


  // --------------------------------------------------------------------
  // RECEIVE CIPHERTEXT
  // --------------------------------------------------------------------
  // Get ciphertext from server
  // first, clear buffer and counter
  if (recv_msg(socket_fd, ciphertext, store_msg, TEXT_BUFFER_SIZE, MSG_BUFFER_SIZE) == -1) {
    error("enc_client: ERROR reading CIPHERTEXT from socket");
  }


  // --------------------------------------------------------------------
  // OUTPUT CIPHERTEXT AND CLOSE CONNECTION
  // --------------------------------------------------------------------
  printf("%s\n", ciphertext);

  // Close the socket
  close(socket_fd); 
  return 0;
}


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
  // append EOM to end of array
  array[strlen(array)] = EOM_CHAR;
  array[strlen(array)] = EOM_CHAR;
}


// error
void 
error(const char *msg) { 
  perror(msg); 
  exit(0); 
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


// get_in_addr
void *get_in_addr(struct sockaddr *sa)
{
  if (sa->sa_family == AF_INET) {
    return &(((struct sockaddr_in*)sa)->sin_addr);
  }

  return &(((struct sockaddr_in6*)sa)->sin6_addr);

} // end of get_in_addr
