#include <stdio.h>

/* util.c */
void *xmalloc(size_t size);
void *xcalloc(size_t nmemb, size_t size);
void *xrealloc(void *p, size_t size);
char *xstrdup(const char *s);
char *xstrndup(const char *s, size_t n);

struct gstr {
	size_t len;
	char  *s;
	/*
	* when max_width is not zero long lines in string s (if any) get
	* wrapped not to exceed the max_width value
	*/
	int max_width;
};
struct gstr str_new(void);
void str_free(struct gstr *gs);
void str_append(struct gstr *gs, const char *s);
void str_printf(struct gstr *gs, const char *fmt, ...);
const char *str_get(struct gstr *gs);
