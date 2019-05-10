#include <stdio.h>
#include "../lib/config_symbol.h"
#include "../lib/lkc.h"

void print_cs_node(struct cs_node *node);
void print_all_node();
void print_all_node()
{
      int i;
      printf("nr_cs: %d\n", nr_cs);
      for (i = 0; i < nr_cs; i++) {
            printf("%d: ", i);
            print_cs_node(cs_table[i]);
      }
}

void print_cs_node(struct cs_node *node)
{
            switch (node->type) {
            case T_STRING:
                  printf("%s = %s\n", node->name, node->data.str);
                  break;
            case T_HEXA:
                  printf("%s = 0x%llX\n", node->name, node->data.ull);
                  break;
            case T_DECIMAL:
                  printf("%s = %llu\n", node->name, node->data.ull);
                  break;
            case T_YES:
                  printf("%s = y\n", node->name);
                  break;
            case T_MODULE:
                  printf("%s = m\n", node->name);
                  break;
            }
}


void func()
{
	struct cs_node *temp;
	static char ch = 'a';
	temp = (struct cs_node *)xmalloc(sizeof(struct cs_node));
	temp->name = (char *)xmalloc(sizeof(10));
	*(temp->name) = (ch += 1);
	temp->data.ull = ch - 'a';
	temp->type = T_HEXA;
	insert_cs_node(temp);
}

int main()
{
	struct cs_node *temp;
	func();
	print_cs_node(cs_table[nr_cs - 1]);
	func();
	print_cs_node(cs_table[nr_cs - 1]);
	func();
	print_cs_node(cs_table[nr_cs - 1]);
	func();
	print_cs_node(cs_table[nr_cs - 1]);
	func();
	print_cs_node(cs_table[nr_cs - 1]);
	func();
	print_cs_node(cs_table[nr_cs - 1]);
	func();
	print_cs_node(cs_table[nr_cs - 1]);

}
