#include "stdlib.h"
#include "memory_manager.h"
#include "interrupts.h"
#include "tty.h"
#include "user.h"

typedef struct {
	uint64 base;
	uint64 size;
} BootModuleInfo;

void kernel_main(uint8 boot_disk_id, void *memory_map, BootModuleInfo *boot_module_list) {
	init_memory_manager(memory_map);
	init_interrupts();
	init_tty();
	set_text_attr(0x1B);

	printf("Welcome to FunOS!\n\n");

	printf("The shell: sh\n");
	printf("Reboot: reboot\n");
	char select[256];


	while (true) {
		in_string(select, strlen(select));

		if (compstr(select, "sh") == 0)
			sh();
		if (compstr(select, "reboot") == 0)
			reboot();
		if (compstr(select, "version") == 0)
			version();
    else
    	printf("Unknown command\n");
	}
}
