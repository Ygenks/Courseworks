#include "user.h"
#include "tty.h"
#include "stdlib.h"

#define OS_NAME "FunOS Education"
#define VERSION_OS "0.0.1"

void reboot(){
	asm("int $0x16");
}

void version(){
	printf("%s ", OS_NAME);
	printf("%s\n", VERSION_OS);
}

void help_sh(){
	printf(" Help:\n");
	printf("  clear - clear screen:\n");
	printf("  version - the kernel version:\n");

}

void easter() {

  printf("                      ___    _____\n");
  printf("                     /   \\  / ___/\n");
  printf("                    |     |(   \\__ \n");
  printf("                    |  O  | \\__   \\\n");
  printf("___  ___  __        |     | /  \\   |\n");
  printf(" |  |__  |__)  |\\/| |     ! \\     /\n");
  printf(" |  |___ |  \\  |  |  \\___/   \\___/\n");

}

void sh(){
	set_text_attr(0x1B);
	printf("Shell 0.1\n");
	printf("Enter help for help\n");
	char com_name[50];
	while((compstr(com_name, "quit") != 0)){
		out_char('$', false);
		out_char(' ', false);
		in_string(com_name, strlen(com_name));

		if (compstr(com_name, "clear") == 0)
			clear_screen();
		if (compstr(com_name, "version") == 0)
			version();
		if (compstr(com_name, "help") == 0)
			help_sh();
    if(compstr(com_name, "vmsis") == 0)
      easter();
    if(compstr(com_name, "reboot") == 0)
      reboot();
	}
	set_text_attr(0x1B);
	clear_screen();
}
