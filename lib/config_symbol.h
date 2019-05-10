#ifndef __CS_H__
#define __CS_H__

/* Error Code */
#define EEXCLU 0x1 /* Exclude */
#define ENOINI 0x2 /* No Init */
#define EDUPLI 0x2 /* Duplication */

enum cs_types {
      T_YES,
      T_MODULE,
      T_STRING,
      T_HEXA,
      T_DECIMAL,
      T_COUNT
};

struct cs_node {
      char *name;
      enum cs_types type;
      union {
            unsigned long long int ull;
            char *str;
      } data;
};

struct cs_node **cs_table;
int nr_cs;

#define INIT_CS_TABLE() init_cs_table()

void init_cs_table();
int insert_cs_node(struct cs_node *);
int search_cs_node(char *, struct cs_node *);


#endif
