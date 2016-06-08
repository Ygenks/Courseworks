
#ifndef TTY_H
#define TTY_H

#include "stdlib.h"

void init_tty();
void out_char(char chr, bool printf_mode);
void out_string(char *str, bool printf_mode);
void clear_screen();
void set_text_attr(char attr);
void move_cursor(unsigned int pos);
void printf(char *fmt, ...);
char in_char(bool wait);
void in_string(char *buffer, size_t buffer_size);

#endif
